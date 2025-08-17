from __future__ import annotations

import asyncio
import base64
import io
from typing import Any

from celeste_core import ImageArtifact
from celeste_core.base.image_editor import BaseImageEditor
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from celeste_core.models.registry import supports
from openai import OpenAI


class OpenAIImageEditor(BaseImageEditor):
    def __init__(self, model: str = "gpt-image-1", **kwargs: Any) -> None:
        # Base initializer intentionally not called because it's abstract
        self.client = OpenAI(api_key=settings.openai.api_key)
        self.model_name = model
        # Non-raising validation; store support state for callers to inspect
        self.is_supported = supports(self.model_name, Capability.IMAGE_EDIT)

    async def edit_image(
        self, prompt: str, image: ImageArtifact, **kwargs: Any
    ) -> ImageArtifact:
        def _edit_sync() -> bytes:
            # Handle file path vs raw bytes
            if image.path:
                with open(image.path, "rb") as img_file:
                    resp = self.client.images.edit(
                        model=self.model_name,
                        image=img_file,
                        prompt=prompt,
                        size=kwargs.get("size", "1024x1024"),
                        # quality only for some models; pass-through if provided
                        **(
                            {"quality": kwargs["quality"]}
                            if "quality" in kwargs
                            else {}
                        ),
                    )
            else:
                resp = self.client.images.edit(
                    model=self.model_name,
                    image=io.BytesIO(image.data),
                    prompt=prompt,
                    size=kwargs.get("size", "1024x1024"),
                    # quality only for some models; pass-through if provided
                    **({"quality": kwargs["quality"]} if "quality" in kwargs else {}),
                )
            b64 = resp.data[0].b64_json
            return base64.b64decode(b64)

        image_bytes = await asyncio.to_thread(_edit_sync)

        return ImageArtifact(
            data=image_bytes,
            metadata={
                "model": self.model_name,
            },
        )
