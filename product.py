from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import main
from typing import List

router = APIRouter(prefix="/products", tags=['Products'])
@router.get("/",response_model=List[main.ProductOut])
async def get_all_product(db:AsyncSession=Depends(get_db)):
    result = await main.get_products(db)
    return  result


@router.get("/filter/{word}",response_model=List[main.ProductOut])
async def filter_by_category_with_keyword(word:str,db:AsyncSession=Depends(get_db)):
    results=[]
    products = await main.get_products(db)
    for product in products:
        if word.lower() in product.category.lower():
            results.append(product)
    return results

@router.get("/filter/{word}",response_model=List[main.ProductOut])
async def filter_by_category_with_keyword(word:str,db:AsyncSession=Depends(get_db)):
    results=[]
    products = await main.get_products(db)
    for product in products:
        if word.lower() in product.category.lower():
            results.append(product)
    return results

@router.get("/search/{product_keyword}",response_model=List[main.ProductOut])
async def search_by_product_keyword(product_keyword:str,db:AsyncSession=Depends(get_db)):
    results = []
    products = await main.get_products(db)
    for product in products:
        if product_keyword.lower() in product.name.lower():
            results.append(product)
    return results

from sqlalchemy.future import select
from datetime import datetime
@router.get("/filter/{from_date}/{to_date}",response_model=List[main.ProductOut])
async def filter_product_by_dates(from_date:str,to_date:str,db:AsyncSession=Depends(get_db)):
    # results =[]
    # products = await get_products(db)
    # for product in products:
    #     if from_date <= product.date >=to_date:
    #         results.append(product)
    # if results:
    #     return results
    # return "No Product found"
    from datetime import date
    def normalize(d: str) -> date:
        return datetime.strptime(d, "%Y-%m-%d").date()

    from_date = normalize(from_date)
    to_date = normalize(to_date)
    # Ensure correct ordering
    if from_date > to_date:
        from_date, to_date = to_date, from_date

    query = select(main.Product).where(main.Product.date.between(from_date,to_date))
    result =await db.execute(query)
    return result.scalars().all()

from sqlalchemy import select, desc, and_

from pydantic import BaseModel

class ProductNamePrice(BaseModel):
    name: str
    price: float
    category: str
@router.get("/filter/price/{max_price}/{min_price}",response_model=List[ProductNamePrice])
async def product_filter_by_maximum_price(max_price:float,min_price:float,db:AsyncSession=Depends(get_db)):
    # results =[]
    # products = await get_products(db)
    # for product in products:
    #     product.price <= max_price
    #     results.append(product)
    # if results:
    #     return results
    # return "No product found"

    query = (select(main.Product.name, main.Product.price,main.Product.category)
             .where(and_(main.Product.price <= max_price, main.Product.price >= min_price))
             .order_by(desc(main.Product.price)))
    result = await db.execute(query)
    return result.all()
