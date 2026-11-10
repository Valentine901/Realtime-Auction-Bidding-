from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import setting


class Base(DeclarativeBase):
    pass 

engine = create_async_engine(setting.DATABASE_URL)

