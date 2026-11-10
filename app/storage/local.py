import asyncio 
from pathlib import Path 
from uuid import uuid4, uuid3

from app.storage.base import ImageStorage


class LocalImageStorage(ImageStorage):
    def __init__(self, folder: Path, base_url: str = "/uploads"):
        self.folder = folder 
        self.base_url = base_url
        self.folder.mkdir(parents=True, exist_ok=True)

    async def save(self, content: bytes, extension: str) -> str:
        filename = f"{uuid4().hex}.{extension}"

        # Path objects use "/" to join. This builds folder\filename
        path = self.folder / filename 

        # write_bytes is a normal blocking call. It would freeze the whole server while writing. to_thread runs it on the worker thread while processing other requests
        await asyncio.to_thread(path.write_bytes, content)

        return f"{self.base_url}/{filename}"

