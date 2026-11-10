from app.repositories.product import ProductRepository
from app.services.product import ProductService
from app.models import Product 


async def test_product(session):
    

    p1 = Product(
        name="product1",
        image="no image",
        desc="no desc",
        seller_id=1
    )
    session.add(p1)
    await session.commit()

    data = ProductRepository(session)
    products = await data.list_by_seller(seller_id=1, skip=0, limit=1)
    assert len(products) == 1




# async def test_fetch_product(session):
