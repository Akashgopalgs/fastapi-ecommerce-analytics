from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List
from datetime import date
import pandas as pd

from database import engine, Base, get_db
from database_models import Product
from curd import create_product, get_products
from datetime import datetime

app = FastAPI()


# Create tables on startup (async)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def greet():
    return "Welcome to the home page"


@app.post("/load-products")
async def load_products(db: AsyncSession = Depends(get_db)):
    df = pd.read_csv(r"C:\Users\akash\Desktop\amazon_sales_data 2025.csv")

    for _, row in df.iterrows():
        # Convert string like "14-03-2025" into a proper datetime.date
        date_obj = datetime.strptime(row["date"], "%d-%m-%Y").date()
        product_data = {
            "id": str(row["id"]),  # remove this key if you want auto-increment
            "date": date_obj,
            "name": row["name"],
            "category": row["category"],
            "price": float(row["price"]),
            "quantity": int(row["quantity"]),
            "total_sales": int(row["total sales"]),
            "customer_name": row["customer name"],
            "status": row["status"],
            "customer_location": row["customer location"],
            "payment_method": row["payment method"],
        }

        await create_product(db, product_data)

    return {"status": "products loaded"}


class ProductOut(BaseModel):
    id: str
    date: date
    name: str
    category: str
    price: float
    quantity: int
    total_sales: int
    customer_name: str
    customer_location: str
    payment_method: str
    status: str

    class Config:
        orm_mode = True


# @app.get("/products", response_model=List[ProductOut])
# async def list_products(db: AsyncSession = Depends(get_db)):
#     products = await get_products(db)
#     return products



import product,customer
app.include_router(customer.router)
app.include_router(product.router)
# app.include_router(user.router)











# @app.get("/products/filter/{word}",response_model=List[ProductOut])
# async def filter_by_category_with_keyword(word:str,db:AsyncSession=Depends(get_db)):
#     results=[]
#     products = await get_products(db)
#     for product in products:
#         if word.lower() in product.category.lower():
#             results.append(product)
#     return results
#
# @app.get("/products/search/{product_keyword}",response_model=List[ProductOut])
# async def search_by_product_keyword(product_keyword:str,db:AsyncSession=Depends(get_db)):
#     results = []
#     products = await get_products(db)
#     for product in products:
#         if product_keyword.lower() in product.name.lower():
#             results.append(product)
#     return results
#
# from sqlalchemy.future import select
# from datetime import datetime
# @app.get("/products/filter/{from_date}/{to_date}",response_model=List[ProductOut])
# async def filter_product_by_dates(from_date:str,to_date:str,db:AsyncSession=Depends(get_db)):
#     # results =[]
#     # products = await get_products(db)
#     # for product in products:
#     #     if from_date <= product.date >=to_date:
#     #         results.append(product)
#     # if results:
#     #     return results
#     # return "No Product found"
#     def normalize(d: str) -> date:
#         return datetime.strptime(d, "%Y-%m-%d").date()
#
#     from_date = normalize(from_date)
#     to_date = normalize(to_date)
#     # Ensure correct ordering
#     if from_date > to_date:
#         from_date, to_date = to_date, from_date
#
#     query = select(Product).where(Product.date.between(from_date,to_date))
#     result =await db.execute(query)
#     return result.scalars().all()
#
# from sqlalchemy import select, desc, and_
#
# from pydantic import BaseModel
#
# class ProductNamePrice(BaseModel):
#     name: str
#     price: float
#     category: str
# @app.get("/products/filter/price/{max_price}/{min_price}",response_model=List[ProductNamePrice])
# async def product_filter_by_maximum_price(max_price:float,min_price:float,db:AsyncSession=Depends(get_db)):
#     # results =[]
#     # products = await get_products(db)
#     # for product in products:
#     #     product.price <= max_price
#     #     results.append(product)
#     # if results:
#     #     return results
#     # return "No product found"
#
#     query = (select(Product.name, Product.price,Product.category)
#              .where(and_(Product.price <= max_price, Product.price >= min_price))
#              .order_by(desc(Product.price)))
#     result = await db.execute(query)
#     return result.all()
#
# # @app.get('/products/')
