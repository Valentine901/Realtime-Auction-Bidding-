from app.core.exceptions import UserNotFound, EmailAlreadyRegistered, InvalidCredentials
from app.models import User 
from app.repositories.user import UserRepository
from app.core.security import hash_password, verify_password

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo 

    async def get_user(self, user_id: int) -> User:
        user = await self.repo.get_by_id(id_=user_id)
        if user is None: 
            raise UserNotFound
        return user 

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)
        
        if user is None or not verify_password(password, user.password):
            raise InvalidCredentials

        return user

    async def register(self, fullname: str, email: str, password: str) -> User:
        # normalize_email = email.split("@")[-1]
        existing = await self.repo.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyRegistered

        # data = {
        #     "fullname": fullname,
        #     "email": email,
        #     "password": hash_password(password)
        # }
        # await self.repo.create(**data)
        user = await self.repo.create(
            fullname=fullname,
            email=email,
            password=hash_password(password)
        )

        await self.repo.commit()
        return user 