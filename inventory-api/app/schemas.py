from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(..., gt=0)

class ProductCreate(ProductBase):
    available_quantity: int = Field(0, ge=0)

class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)

class Product(ProductBase):
    id: int
    available_quantity: int
    class Config:
        from_attributes = True

class StockTransactionBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    transaction_type: TransactionType

class StockTransactionCreate(StockTransactionBase):
    pass

class StockTransaction(StockTransactionBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True