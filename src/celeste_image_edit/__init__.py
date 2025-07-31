"""
Celeste Image Generation: A unified image generation interface for multiple providers.
"""

from typing import Any

from .base import BaseImageEditor

from .core.enums import ImageEditProvider
from .core.types import Image

__version__ = "0.1.0"

SUPPORTED_PROVIDERS = [
    "google",
    "openai",
    "replicate",
]


def create_image_editor(provider: str, **kwargs: Any) -> BaseImageEditor:
    """
    Factory function to create an image generator instance based on the provider.

    Args:
        provider: The image generator provider to use (string or Provider enum).
        **kwargs: Additional arguments to pass to the image generator constructor.

    Returns:
        An instance of an image generator
    """
    # Convert Provider enum to string if needed
    if isinstance(provider, ImageEditProvider):
        provider = provider.value

    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")

    if provider == "google":
        from .providers.google import GoogleImageEditor
        return GoogleImageEditor(**kwargs)
    
    if provider == "openai":
        from .providers.openai import OpenAIImageEditor
        return OpenAIImageEditor(**kwargs)
    
    if provider == "replicate":
        from .providers.replicate import ReplicateImageEditor
        return ReplicateImageEditor(**kwargs)

    raise ValueError(f"Provider {provider} not implemented")


__all__ = [
    "create_image_editor",
    "BaseImageEditor",
    "ImageEditProvider",
    "Image",
    "__version__",
]
