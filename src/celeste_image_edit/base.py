from abc import ABC, abstractmethod
from typing import Any, List

from celeste_image_edit.core.types import Image


class BaseImageEditor(ABC):
    """
    Abstract base class for all image edition clients.
    It defines the standard interface for interacting with different image providers.
    """

    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the client, loading credentials from the environment.
        Provider-specific arguments can be passed via kwargs.
        """
        pass

    @abstractmethod
    async def edit_image(self, prompt: str, image: Image, **kwargs: Any) -> Image:
        """
        Submits a request to start an image edition job.
        """
        pass

