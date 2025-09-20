from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    token_balance: int

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cost: int

class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    cost: int
    owner_name: str
    owner_email: str

class SpendIn(BaseModel):
    product_id: int

class EarnIn(BaseModel):
    amount: int