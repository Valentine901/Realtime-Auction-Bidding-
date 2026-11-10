from abc import ABC, abstractmethod

class ImageStorage(ABC):

    @abstractmethod
    async def save(self, content: bytes, extension: str) -> str:
        """Stores the image as bytes and returns the URL"""

class Broken(ImageStorage):

    async def save(self, content, extension) -> str:
        return ""

Broken()