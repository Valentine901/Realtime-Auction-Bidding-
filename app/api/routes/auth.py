from fastapi import APIRouter, Depends, Response

from app.api.deps import get_user_service
from app.core.config import setting
from app.core.security import create_access_token
from app.schemas.user import UserLogin, UserRead, UserCreate
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserRead, status_code=200)
async def login (
    payload: UserLogin,
    response: Response, 
    service: UserService = Depends(get_user_service)
):
    user = await service.authenticate(payload.email, payload.password)

    token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax", #Block most forge cross-site request
        max_age=60*60*24
    )

    return user

@router.post("/register", response_model=UserRead, status_code=201)
async def register(
    payload: UserCreate,
    response: Response, 
    service: UserService = Depends(get_user_service)
):
    user = await service.register(payload.fullname, payload.email, payload.password)

    token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax", #Block most forge cross-site request
        max_age=60*60*24
    )

    return user

@router.post("/logout", status_code=204)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    