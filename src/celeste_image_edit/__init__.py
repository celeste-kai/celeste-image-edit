"""
Celeste Image Generation: A unified image generation interface for multiple providers.
"""

from typing import Any

from celeste_core import Provider, list_models
from celeste_core.base.image_editor import BaseImageEditor
from celeste_core.config.settings import settings
from celeste_core.enums.capability import Capability

__version__ = "0.1.0"


def create_image_editor(provider: str | Provider, **kwargs: Any) -> BaseImageEditor:
    """
    Factory function to create an image generator instance based on the provider.

    Args:
        provider: The image generator provider to use (string or Provider enum).
        **kwargs: Additional arguments to pass to the image generator constructor.

    Returns:
        An instance of an image generator
    """
    provider_enum: Provider = (
        provider if isinstance(provider, Provider) else Provider(provider)
    )

    # Ensure there is at least one registered model for this provider/capability
    if not list_models(provider=provider_enum, capability=Capability.IMAGE_EDIT):
        msg = f"No models for provider {provider_enum} with capability IMAGE_EDIT"
        raise ValueError(msg)

    # Validate environment for the chosen provider
    settings.validate_for_provider(provider_enum.value)

    mapping = {
        Provider.GOOGLE: (".providers.google", "GoogleImageEditor"),
        Provider.REPLICATE: (".providers.replicate", "ReplicateImageEditor"),
        Provider.OPENAI: (".providers.openai", "OpenAIImageEditor"),
    }

    if provider_enum not in mapping:
        raise ValueError(f"No editor mapping for provider: {provider_enum}")
    module_path, class_name = mapping[provider_enum]
    module = __import__(f"celeste_image_edit{module_path}", fromlist=[class_name])
    editor_class = getattr(module, class_name)
    return editor_class(**kwargs)


__all__ = [
    "create_image_editor",
    "BaseImageEditor",
    "Provider",
    "__version__",
]
