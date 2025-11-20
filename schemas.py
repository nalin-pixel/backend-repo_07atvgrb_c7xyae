"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (you can keep these for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# App-specific schemas
# --------------------------------------------------

class Listing(BaseModel):
    """
    Second-hand clothing listing
    Collection name: "listing"
    """
    title: str = Field(..., description="Listing title")
    description: Optional[str] = Field(None, description="Item description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Category like Dresses, Tops, Bottoms, Outerwear, Shoes, Accessories")
    size: Optional[str] = Field(None, description="Size like XS, S, M, L, XL, or numeric")
    brand: Optional[str] = Field(None, description="Brand name")
    condition: Optional[str] = Field(None, description="Condition like New, Like New, Good, Fair")
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")
    location: Optional[str] = Field(None, description="Seller location")
