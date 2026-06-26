# app/schemas/product.py
from typing import Optional
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0
    category: str
    description: Optional[str] = None