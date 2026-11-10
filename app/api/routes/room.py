from fastapi import Depends, APIRouter, Query
from app.api.deps import get_room_service, get_current_user 
from app.services.room import RoomService 
from app.schemas.room import RoomRead, RoomCreate
from app.models import User 
from app.realtime.manager import manager 

from typing import List

router = APIRouter(prefix="/rooms", tags=["room"])

@router.post("", response_model=RoomRead, status_code=201)
async def create_room(
    payload: RoomCreate,
    service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user)
):
    return await service.create_room(
        name=payload.name,
        creator_id=current_user.id
    )

@router.get("/{room_id}/room", response_model=RoomRead)
async def get_room(room_id: int, service: RoomService = Depends(get_room_service)):
    return await service.get_room(room_id)

@router.get("", response_model=List[RoomRead])
async def list_rooms(
    skip: int = Query(0, ge=0), 
    limit: int = Query(20, ge=1, le=100), 
    service: RoomService = Depends(get_room_service)
    ):
    return await service.get_active_rooms(
        skip=skip,
        limit=limit
    )

@router.post("/{room_id}/close", response_model=RoomRead)
async def close_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    current_user: User = Depends(get_current_user)
):
    room = await service.close_room(room_id, current_user.id)

    await manager.close_room(room_id, {"type":"room_closed", "room_id": room_id})

    return room