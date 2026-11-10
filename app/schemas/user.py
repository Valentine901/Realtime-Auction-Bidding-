from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    """Request from client"""
    fullname: str = Field(min_length=3, max_length=30)
    email: EmailStr 
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr 
    password: str

class UserRead(BaseModel):
    """Response sent back to client"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    fullname: str 
    email: EmailStr 