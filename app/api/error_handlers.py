from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse

from app.core.exceptions import *



def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(InvalidToken)
    async def invalid_token_handler(request: Request, exc: InvalidToken):
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    @app.exception_handler(RoomInactive)
    async def inactive_room_handler(request: Request, exc: RoomInactive):
        return JSONResponse(status_code=400, content={"detail": "Room is inactive"})
    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request: Request, exc: UserNotFound):
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    @app.exception_handler(RoomNotFound)
    async def room_not_found(request: Request, exc: RoomNotFound):
        return JSONResponse(status_code=404, content={"detail":"Room not found"})


    @app.exception_handler(NotRoomOwner)
    async def not_room_owner_handler(request: Request, exc: NotRoomOwner):
        return JSONResponse(status_code=403, content={"detail": "You do not own this room"})

    @app.exception_handler(RoomNameTaken)
    async def room_name_taken_handler(request: Request, exc: RoomNameTaken):
        return JSONResponse(status_code=409, content={"detail": "Room name already taken"})

    @app.exception_handler(EmailAlreadyRegistered)
    async def email_taken_handler(request: Request, exc: EmailAlreadyRegistered):
        return JSONResponse(status_code=409, content={"detail": "Email already registered"})

    @app.exception_handler(ProductNotFound)
    async def product_not_found_handler(request: Request, exc: ProductNotFound):
        return JSONResponse(status_code=404, content={"detail": "Product not found"})

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentials):
        return JSONResponse(status_code=401, content={"detail": "Invalid email or password"})

