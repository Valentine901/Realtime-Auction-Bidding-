from typing import TypeVar, Generic
from app.db.base import Base 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from typing import Sequence, List

ModelT = TypeVar("ModelT", bound=Base)

class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession):
        self.session = session
        self.model = model

    async def _get_one(self, *args) -> ModelT | None:
        query = select(self.model).where(*args)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def _get_many(self, *args, skip: int = 0, limit: int = 20) -> Sequence[ModelT]:
        query = (
            select(self.model)
            .where(*args)
            .order_by(self.model.id)
            .offset(skip)
            .limit(limit)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    
    async def create(self, **kwargs) -> ModelT:
        obj = self.model(**kwargs)
        self.session.add(obj)

        # flush = send the INSERT to the database NOW, so the database assigns the id.
        await self.session.flush()
        return obj
    
    async def commit(self) -> None:
        await self.session.commit()

    async def get_by_id(self, id_: int) -> ModelT | None:
        return await self.session.get(self.model, id_)