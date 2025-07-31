from typing import Any, List

from google import genai

import PIL
import io

from google.genai import types

from celeste_image_edit.base import BaseImageEditor
from celeste_image_edit.core.config import GOOGLE_API_KEY
from celeste_image_edit.core.enums import GoogleEditModel
from celeste_image_edit.core.types import Image

class GoogleImageEditor(BaseImageEditor):
    def __init__(self, model: str = GoogleEditModel.FLASH_2_0_PREVIEW_IMAGEN.value, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model_name = model

    async def edit_image(self, prompt: str, image: Image, **kwargs: Any) -> Image:

        if image.path:
            img = PIL.Image.open(image.path)
        else:
            img = PIL.Image.open(io.BytesIO(image.data))

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents = [prompt, img],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE','TEXT']
            )
        )


        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                return Image(
                    data=part.inline_data.data,
                    metadata={
                        "model": response.model_version,
                        "total_tokens": response.usage_metadata.total_token_count
                    }
                )
        
        return None
