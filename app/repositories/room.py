from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models import Room 


class RoomRepository(BaseRepository[Room]):
    def __init__(self, session: AsyncSession):
        super().__init__(Room, session)

    async def get_room_by_name(self, name: str) -> Room | None:
        return await self._get_one(Room.name == name)

    async def list_active(self, skip: int = 0, limit: int = 20) -> Sequence[Room]:
        # Room.is_active.is_(True) builds the SQL condition "is_active IS 1".
        # Why not "Room.is_active == True"? It works, but linters flag it, and .is_(True)
        # is SQLAlchemy's recommended way to compare against a boolean.
        return await self._get_many(
            Room.is_active.is_(True),
            skip=skip,
            limit=limit
    )