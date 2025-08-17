import io
from typing import Any

import PIL
from celeste_core import ImageArtifact
from celeste_core.base.image_editor import BaseImageEditor
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability
from celeste_core.models.registry import supports
from google import genai
from google.genai import types


class GoogleImageEditor(BaseImageEditor):
    def __init__(
        self, model: str = "gemini-2.0-flash-preview-image-generation", **kwargs: Any
    ) -> None:
        self.client = genai.Client(api_key=settings.google.api_key)
        self.model_name = model
        self.is_supported = supports(self.model_name, Capability.IMAGE_EDIT)

    async def edit_image(
        self, prompt: str, image: ImageArtifact, **kwargs: Any
    ) -> ImageArtifact:
        if image.path:
            img = PIL.Image.open(image.path)
        else:
            img = PIL.Image.open(io.BytesIO(image.data))

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=[prompt, img],
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                return ImageArtifact(
                    data=part.inline_data.data,
                    metadata={
                        "model": response.model_version,
                        "total_tokens": getattr(
                            response.usage_metadata, "total_token_count", 0
                        ),
                    },
                )

        # Non-raising: return empty artifact if provider returned no image
        return ImageArtifact(data=None, metadata={"model": self.model_name})
