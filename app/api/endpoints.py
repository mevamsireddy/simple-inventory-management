from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import crud, schemas
from ..database import get_db

product_router = APIRouter(prefix="/products", tags=["Products"])
stock_router = APIRouter(prefix="/stock", tags=["Stock"])

@product_router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_product(db=db, product=product)

@product_router.get("/", response_model=List[schemas.Product])
async def list_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_products(db, skip=skip, limit=limit)

@product_router.get("/{product_id}", response_model=schemas.Product)
async def get_product_details(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

@product_router.put("/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    db_product = await crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return await crud.update_product(db=db, db_product=db_product, product_update=product)

@product_router.delete("/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

@stock_router.post("/", response_model=schemas.StockTransaction, status_code=status.HTTP_201_CREATED)
async def record_stock_transaction(transaction: schemas.StockTransactionCreate, db: AsyncSession = Depends(get_db)):
    result = await crud.create_stock_transaction(db=db, transaction=transaction)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result

@stock_router.get("/", response_model=List[schemas.StockTransaction])
async def list_all_stock_transactions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_stock_transactions(db, skip=skip, limit=limit)

@stock_router.get("/product/{product_id}", response_model=List[schemas.StockTransaction])
async def get_product_transactions(product_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    db_product = await crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return await crud.get_stock_transactions_by_product(db, product_id=product_id, skip=skip, limit=limit)