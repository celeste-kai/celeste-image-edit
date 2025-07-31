from enum import Enum


class ImageEditProvider(Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    REPLICATE = "replicate"


class GoogleEditModel(Enum):
    FLASH_2_0_PREVIEW_IMAGEN = "gemini-2.0-flash-preview-image-generation"
    FLASH_2_0_EXP_IMAGEN = "gemini-2.0-flash-exp-image-generation"
    FLASH_2_0_EXP = "gemini-2.0-flash-exp"


class OpenAIEditModel(Enum):
    GPT_IMAGE_1 = "gpt-image-1"


class ReplicateEditModel(Enum):
    FLUX_KONTEXT_PRO = "black-forest-labs/flux-kontext-pro"
    FLUX_KONTEXT_MAX = "black-forest-labs/flux-kontext-max"

