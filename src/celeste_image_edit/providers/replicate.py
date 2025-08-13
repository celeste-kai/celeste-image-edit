from __future__ import annotations

import io
from typing import Any

import replicate
from celeste_core import ImageArtifact
from celeste_core.base.image_editor import BaseImageEditor
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from celeste_core.models.registry import supports


class ReplicateImageEditor(BaseImageEditor):
    def __init__(
        self, model: str = "black-forest-labs/flux-kontext-pro", **kwargs: Any
    ) -> None:
        self.client = replicate.Client(api_token=settings.replicate.api_token)
        self.model_name = model
        # Guard against non-edit models (e.g., qwen/qwen-image is generation-only)
        if not supports(self.model_name, Capability.IMAGE_EDIT):
            raise ValueError(f"Model '{self.model_name}' does not support IMAGE_EDIT")

    async def edit_image(
        self, prompt: str, image: ImageArtifact, **kwargs: Any
    ) -> ImageArtifact:
        # Choose the most likely input key; allow override,
        # but we will fallback across common keys
        preferred_key: str | None = kwargs.pop("input_key", None)
        default_key = "input_image" if "kontext" in self.model_name else "image"
        candidate_keys = [
            k
            for k in [
                preferred_key,
                default_key,
                "image",
                "input_image",
                "image_1",
                "image_url",
                "prompt_image",
                "conditioning_image",
            ]
            if k
        ]

        # Build the image value in the form Replicate expects
        def _prepare_image_value(img: ImageArtifact) -> Any:
            if img.path and img.path.startswith(("http://", "https://")):
                return img.path
            if img.path:
                return open(img.path, "rb")
            buf = io.BytesIO(img.data)  # type: ignore[arg-type]
            if not hasattr(buf, "name"):
                buf.name = "image.png"
            return buf

        # Convert common Replicate outputs to raw bytes and capture URL when present
        def _download(url: str) -> bytes:
            import urllib.request

            with urllib.request.urlopen(url) as resp:
                return resp.read()

        def _first_image_bytes(value: Any) -> tuple[bytes, str | None]:
            # Replicate File-like
            if hasattr(value, "read"):
                url: str | None = None
                if hasattr(value, "url"):
                    try:
                        url = value.url()  # type: ignore[call-arg]
                    except Exception:
                        url = None
                return value.read(), url  # type: ignore[return-value]
            # HTTP URL
            if isinstance(value, str) and value.startswith("http"):
                return _download(value), value
            # List of files/URLs
            if isinstance(value, list) and value:
                for item in value:
                    try:
                        data, url = _first_image_bytes(item)
                        return data, url
                    except Exception:
                        continue
                raise ValueError("Replicate returned list without image content")
            # Dict with common keys
            if isinstance(value, dict):
                for key in ("image", "images", "output", "result"):
                    if key in value:
                        return _first_image_bytes(value[key])
            raise ValueError("Unsupported Replicate output format for image data")

        # Default to PNG unless caller specifies a format
        output_format: str = kwargs.pop("output_format", "png")

        last_err: Exception | None = None
        image_bytes: bytes | None = None
        output_url: str | None = None

        for key in candidate_keys:
            try:
                # Build a fresh image value each attempt to avoid exhausted streams
                image_value = _prepare_image_value(image)

                output = self.client.run(
                    self.model_name,
                    input={
                        "prompt": prompt,
                        key: image_value,
                        "output_format": output_format,
                        **{k: v for k, v in kwargs.items() if v is not None},
                    },
                )
                image_bytes, output_url = _first_image_bytes(output)
                break
            except Exception as e:
                last_err = e
                continue

        if image_bytes is None and last_err is not None:
            raise last_err

        return ImageArtifact(
            data=image_bytes,
            metadata={
                "model": self.model_name,
                **({"output_url": output_url} if output_url else {}),
            },
        )
