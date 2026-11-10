from fastapi import Depends, APIRouter, HTTPException, status, File, UploadFile, Form  
import io
from pathlib import Path
from typing import Annotated
from app.api.deps import get_current_user, get_product_service
from app.schemas.product import ProductRead
from app.models import User 
from app.storage.local import LocalImageStorage
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductRead, status_code=201)
async def create_product(
    name: Annotated[str, Form()],
    desc: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):

    file = LocalImageStorage(folder=Path("images"))
    extension = str(image.filename).split(".")[-1]
    byte_file = await image.read()
    image_path = await file.save(content=byte_file, extension=extension)
    return await service.create_product(
        seller_id=current_user.id,
        name=name,
        image=image_path,
        desc=desc
    )

@router.get("/product/(product_id)", response_model=ProductRead)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    return await service.get_product(product_id=product_id)