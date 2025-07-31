from typing import Optional

from pydantic import BaseModel, model_validator


class ImagePrompt(BaseModel):
    content: str

class Image(BaseModel):
    """Represents a single generated image and its metadata"""
    data: Optional[bytes] = None
    path: Optional[str] = None
    metadata: Optional[dict] = None
    
    @model_validator(mode='after')
    def _check_data_or_path(self):
        if not (self.data or self.path):
            raise ValueError("Either 'data' or 'path' must be provided")
        return self