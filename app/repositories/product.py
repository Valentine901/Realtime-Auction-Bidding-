from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product 
from typing import Sequence

class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def list_by_seller(self, seller_id: int, skip: int = 0, limit: int = 20) -> Sequence[Product]:
        return await self._get_many(Product.seller_id == seller_id, skip=skip, limit=limit)

