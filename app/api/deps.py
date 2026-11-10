from fastapi import Depends, HTTPException, WebSocket, WebSocketException, status
from fastapi.security import APIKeyCookie 
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.security import decode_token
from app.db.session import get_session 

from app.repositories.user import UserRepository
from app.repositories.product import ProductRepository
from app.repositories.room import RoomRepository

from app.services.product import ProductService
from app.services.user import UserService
from app.services.room import RoomService

from app.core.exceptions import UserNotFound, InvalidToken
from app.models import User 


cookie_scheme = APIKeyCookie(name="access_token", auto_error=True)

def get_product_repo(session: AsyncSession = Depends(get_session)):
    return ProductRepository(session)

def get_room_repo(session: AsyncSession = Depends(get_session)):
    return RoomRepository(session)

def get_product_service(repo: ProductRepository = Depends(get_product_repo)):
    return ProductService(repo)

def get_room_service(repo: RoomRepository = Depends(get_room_repo)):
    return RoomService(repo)


def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo)



async def get_current_user_ws(
    websocket: WebSocket,
    service: UserService = Depends(get_user_service)
) -> User: 
    token = websocket.cookies.get("access_token")
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    try:
        payload = decode_token(token)
        user = await service.get_user(payload["sub"])

    except (InvalidToken, UserNotFound, KeyError, ValueError, TypeError):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    return user 


async def get_current_user(token: str = Depends(cookie_scheme), service: UserService = Depends(get_user_service)) -> User:
    payload = decode_token(token)

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user = await service.get_user(user_id)
    except UserNotFound:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user 

