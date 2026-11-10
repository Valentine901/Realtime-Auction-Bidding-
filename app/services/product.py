from app.repositories.product import ProductRepository
from app.models  import Product 
from app.core.exceptions import ProductNotFound

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo 

    
    async def create_product(
            self, seller_id: int, name: str, image: str, desc: str
    ) -> Product:

        product = await self.repo.create(
            seller_id=seller_id,
            name=name,
            image=image,
            desc=desc
        )

        await self.repo.commit()
        return product 

    async def get_product(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(id_=product_id)
        if product is None:
            raise ProductNotFound
        return product