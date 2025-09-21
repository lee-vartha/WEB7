from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# defines the user model class using SQLModel, which is used for interaction with SQL db in python applications (like FastAPI)
# table=true tells SQLModel to create a corresponding database table for this class
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(regex="^(donor|beneficiary)$")
    token_balance: int = 10

    products: list["Product"] = Relationship(back_populates="owner")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    cost: int
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="products")

class TokenRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    amount: int
    type: str = Field(regex="^(earn|spend)$")
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")