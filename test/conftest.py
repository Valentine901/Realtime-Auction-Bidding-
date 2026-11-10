import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.base import Base 
import app.models
import pytest


# fixture is a function prepare something for a test
@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
    )
    

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with TestSessionLocal() as session:
        yield session

    await engine.dispose()


# @pytest.fixture
# def greeting():
#     print("SETUP")
#     yield "hello buddy"
#     print("CLEANUP")