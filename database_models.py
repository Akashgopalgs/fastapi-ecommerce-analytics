from sqlalchemy import Column, String, Integer, Float, Date
from database import Base


class Product(Base):
    __tablename__ = "ecommerse_product"

    id = Column(String, primary_key=True)
    date = Column(Date)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    total_sales = Column(Integer)
    customer_name = Column(String)
    customer_location = Column(String)
    payment_method = Column(String)
    status = Column(String)
