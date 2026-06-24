# app/schemas/product.py
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0
    category: str
    description: str | None = None