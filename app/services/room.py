from app.repositories.room import RoomRepository
from app.core.exceptions import RoomNameTaken, RoomNotFound, NotRoomOwner, RoomInactive 
from app.models import Room

from typing import Sequence

class RoomService:
    def __init__(self, repo: RoomRepository):
        self.repo = repo  

    async def create_room(self, name: str, creator_id: int) -> Room:
        is_existed = await self.repo.get_room_by_name(name)
        if is_existed is not None:
            raise RoomNameTaken
        
        room = await self.repo.create(
            name=name,
            creator_id=creator_id
        )
        await self.repo.commit()

        return room

    async def get_active_room(self, room_id: int) -> Room:
        room = await self.get_room(room_id)

        if not room.is_active:
            raise RoomInactive
        return room

    async def close_room(self, room_id: int, creator_id: int) -> Room:
        room = await self.get_owned_room(room_id, creator_id)

        if not room.is_active:
            return room
        
        room.is_active = False 

        await self.repo.commit()
        return room 

    async def get_room(self, room_id: int) -> Room:
        room = await self.repo.get_by_id(id_=room_id)
        if room is None:
            raise RoomNotFound
        return room 
    
    async def get_active_rooms(self, skip: int = 0, limit: int = 20) -> Sequence[Room]:
        return await self.repo.list_active(skip=skip, limit=limit)

    async def get_owned_room(self, room_id: int, user_id: int) -> Room:
        room = await self.get_room(room_id)
        if room.creator_id != user_id:
            raise NotRoomOwner 
        return room 
