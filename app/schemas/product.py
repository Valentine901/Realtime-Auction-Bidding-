from pydantic import BaseModel, ConfigDict, Field 


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    image: str 
    desc: str = Field(min_length=10)

class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    id: int 
    name: str
    desc: str
    image: str
    is_sold: bool
    seller_id: int 