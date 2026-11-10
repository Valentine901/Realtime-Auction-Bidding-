from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, WebSocketException, status

from app.realtime.manager import manager 
from app.api.deps import get_current_user_ws, get_room_service
from app.models import User 
from app.services.room import RoomService
from app.core.exceptions import RoomInactive, RoomNotFound

router = APIRouter()

@router.websocket("/ws/rooms/{room_id}")
async def room_socket(
    websocket: WebSocket, 
    room_id: int, 
    current_user: User = Depends(get_current_user_ws),
    rooms: RoomService = Depends(get_room_service)
    ):


    try:
        active_room = await rooms.get_active_room(room_id)
    except (RoomNotFound, RoomInactive):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    await manager.connect(room_id, websocket)

    await manager.send_personal(websocket, {
        "type":"personal_message",
        "room": {"id": room_id, "name": active_room.name},
        "online": manager.count_conn(room_id)
    })

    # 
    await manager.broadcast(room_id, {
        "type": "user_joined",
        "user": {
            "id": current_user.id,
            "fullname": current_user.fullname
        },
        "online": manager.count_conn(room_id)
    }, exclude=websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, {
               "type": "user_left",
               "user": {
                   "id": current_user.id,
                   "fullname": current_user.fullname
               },
               "online": manager.count_conn(room_id)
        })