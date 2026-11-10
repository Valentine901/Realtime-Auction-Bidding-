from datetime import datetime 
from pydantic import BaseModel, ConfigDict, Field

class RoomCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=3, max_length=30)

class RoomRead(BaseModel):
    id: int 
    name: str 
    creator_id: int 
    created_at: datetime 
    is_active: bool 

    model_config = ConfigDict(from_attributes=True)