from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.db.base import engine 

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session