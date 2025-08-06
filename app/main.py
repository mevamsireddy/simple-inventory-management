from fastapi import FastAPI
from .api.endpoints import product_router, stock_router

app = FastAPI(
    title="Inventory Management API",
    description="A simple API to manage products and stock movements.",
    version="1.0.0",
)

app.include_router(product_router)
app.include_router(stock_router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Inventory Management API!"}