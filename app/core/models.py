from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class Product(BaseModel):
    """Product model for e-commerce items"""
    id: int
    name: str
    category: str
    subcategory: str
    brand: str
    price: float
    specification: Dict[str, Any]
    availability: bool
    rating: float = Field(ge=0, le=5)
    color: List[str]
    usage: str
    description: str


class ProductSearchParams(BaseModel):
    """Parameters for product search"""
    query: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    color: Optional[str] = None
    availability: Optional[bool] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)


class ProductResponse(BaseModel):
    """Standard response format for products"""
    total: int
    results: List[Product]