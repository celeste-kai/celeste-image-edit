from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider

# Capability for this domain package
CAPABILITY: Capability = Capability.IMAGE_EDIT

# Provider wiring for image editing clients
PROVIDER_MAPPING: dict[Provider, tuple[str, str]] = {
    Provider.GOOGLE: (".providers.google", "GoogleImageEditor"),
    Provider.REPLICATE: (".providers.replicate", "ReplicateImageEditor"),
    Provider.OPENAI: (".providers.openai", "OpenAIImageEditor"),
}

__all__ = ["CAPABILITY", "PROVIDER_MAPPING"]
