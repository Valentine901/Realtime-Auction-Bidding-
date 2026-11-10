from collections import defaultdict
from fastapi import WebSocket 
from typing import Any, Protocol


class Connection(Protocol):

    async def accept(self) -> None: ...
    # The "..." means no code here only the shape of the function is needed

    async def send_json(self, message: Any, /) -> None: ...
    # The "/" mean this parameter is positional only, so it's name doesn't matter

    async def close(self, code: int = 1000) -> None: ... 


class ConnectionManager:
    def __init__(self):
        # The notebook: room number -> the set of lines connected to that room.
        # defaultdict(set) means a new room starts with an empty set automatically.
        self.rooms: dict[int, set[Connection]] = defaultdict(set)

    async def connect(self, room_id: int, websocket: Connection) -> None:
        await websocket.accept()
        self.rooms[room_id].add(websocket)

    def disconnect(self, room_id: int, websocket: Connection) -> None:
        self.rooms[room_id].discard(websocket)
    
    async def send_personal(self, websocket: Connection, message: dict) -> None:
        await websocket.send_json(message)
        return None

    def count_conn(self, room_id: int) -> int:
        total = len(self.rooms[room_id])
        return total

    async def broadcast(self, room_id: int, message: dict, exclude: Connection | None = None) -> None:
        # list(...) makes a COPY first. Below, we may remove a broken line from the set,
        # and Python doesn't allow changing a set while you're looping over it. so we need to convert to list before making any changes on it
        for websocket in list(self.rooms[room_id]):
            if websocket is exclude:
                continue #skip the connection while sending general new conn msg
            try:
                # send message to every live line
                await websocket.send_json(message)
            except Exception:
                # if line dies but we try to send, raise and error and drop their conn
                self.disconnect(room_id, websocket)

    async def close_room(self, room_id: int, message: dict) -> None:
        await self.broadcast(room_id, message)

        lines = self.rooms.pop(room_id, set())

        for websocket in list(lines):
            try:
                await websocket.close(code=1000) # 1000 = "normal closure" nothing went wrong 
            except Exception:
                pass

manager = ConnectionManager()