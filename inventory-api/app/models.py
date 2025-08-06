import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Enum as SQLAlchemyEnum,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .database import Base

class TransactionType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    available_quantity = Column(Integer, default=0)
    stock_movements = relationship("StockTransaction", back_populates="product", cascade="all, delete-orphan")

class StockTransaction(Base):
    __tablename__ = "stock_transactions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_type = Column(SQLAlchemyEnum(TransactionType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="stock_movements")