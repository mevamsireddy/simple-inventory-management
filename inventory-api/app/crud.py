from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas

# --- Product CRUD Functions ---

async def get_product(db: AsyncSession, product_id: int):
    """Fetches a single product by its ID."""
    result = await db.execute(select(models.Product).filter(models.Product.id == product_id))
    return result.scalar_one_or_none()


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Fetches a list of products with pagination."""
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    return result.scalars().all()


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    """Creates a new product and commits it to the database."""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, db_product: models.Product, product_update: schemas.ProductUpdate):
    """Updates an existing product's fields."""
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    """Deletes a product from the database."""
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product


# --- StockTransaction CRUD Functions ---

async def get_stock_transactions(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Fetches all stock transactions with pagination."""
    result = await db.execute(select(models.StockTransaction).offset(skip).limit(limit))
    return result.scalars().all()


async def get_stock_transactions_by_product(db: AsyncSession, product_id: int, skip: int = 0, limit: int = 100):
    """Fetches all stock transactions for a specific product."""
    result = await db.execute(select(models.StockTransaction).filter(models.StockTransaction.product_id == product_id).offset(skip).limit(limit))
    return result.scalars().all()


async def create_stock_transaction(db: AsyncSession, transaction: schemas.StockTransactionCreate):
    """Creates a stock transaction and updates the product's available quantity."""
    db_product = await get_product(db, transaction.product_id)
    if not db_product:
        return None
    if transaction.transaction_type == schemas.TransactionType.OUT:
        if db_product.available_quantity < transaction.quantity:
            return {"error": "Insufficient stock"}
    if transaction.transaction_type == schemas.TransactionType.IN:
        db_product.available_quantity += transaction.quantity
    else:
        db_product.available_quantity -= transaction.quantity
    db_transaction = models.StockTransaction(**transaction.model_dump())
    db.add(db_product)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction