from app.repositories.room import RoomRepository
from app.services.room import RoomService 
from app.core.exceptions import RoomNotFound, RoomInactive, NotRoomOwner
from app.models import Room
import pytest

async def test_get_room_name(session):
    repo = RoomRepository(session)
    session.add(Room(name="valentine", creator_id=1))
    session.add(Room(name="john", creator_id=2))
    await session.commit()
    room = await repo.get_room_by_name(name="valentine")
    assert room.name == "valentine"
    assert room is not None

async def test_room_list(session):
    repo = RoomRepository(session)
    rooms = await repo.list_active(skip=0, limit=20)
    assert rooms == []



async def test_room_close(session):
    repo = RoomRepository(session)
    service = RoomService(repo)
    room = Room(name="valentine", creator_id=1)
    session.add(room)
    await session.commit()

    await service.close_room(room.id, 1)

    await session.rollback()

    saved = await repo.get_by_id(room.id)
    assert saved is not None
    assert saved.is_active is False


async def test_room_refuse_not_owner(session):
    repo = RoomRepository(session)
    service = RoomService(repo)
    room = Room(name="valentine", creator_id=1)
    session.add(room)
    await session.commit()

    with pytest.raises(NotRoomOwner):
        await service.close_room(room.id, 2)

async def test_close_room_not_found(session):
    repo = RoomRepository(session)
    service = RoomService(repo)
    room = Room(name="valentine", creator_id=1)
    session.add(room)
    await session.commit()

    with pytest.raises(RoomNotFound):
        await service.close_room(room.id + 488, 1)

