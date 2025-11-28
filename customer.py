from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import main,curd,database
from typing import List

from sqlalchemy import select,func,desc

router = APIRouter(prefix="/customer",tags=["Customers"])


from pydantic import BaseModel
class CustomerLocationCount(BaseModel):
    customer_location: str
    total_customers: int


@router.get("/user",response_model=List[CustomerLocationCount])
async def most_customer_by_contry(db:AsyncSession=Depends(get_db)):

    query = (select(main.Product.customer_location,func.count(main.Product.customer_name).label("total_customers"))
             .group_by(main.Product.customer_location)).order_by(desc("total_customers"))

    result = await db.execute(query)
    return result.all()

class Customer_order_count(BaseModel):
    customer_name:str
    no_of_orders:int

@router.get("/mostorder",response_model=List[Customer_order_count])
async def most_ordered_customer(db:AsyncSession=Depends(get_db)):

    query = (select(main.Product.customer_name,func.count(main.Product.id).label("no_of_orders"))
             .group_by(main.Product.customer_name).order_by(desc("no_of_orders")))
    result = await db.execute(query)
    return result.all()