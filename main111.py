from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def greet():
    return "Hi Welcome"

from database_models import Product
products = [
    Product(id=1, name="Phone", description="budget phone", price=20000, quantity=5),
    Product(id=2, name="Laptop", description="gaming lap", price=35000, quantity=21),
    Product(id=3, name="earpod", description="budget earpod", price=2200, quantity=6),
    Product(id=4, name="speeker", description="boat speeker", price=2000, quantity=2),

    Product(id=6, name="Phone", description="budget phone budget", price=15000, quantity=15),
    Product(id=7, name="Laptop", description="gaming lap budget", price=30000, quantity=5),
    Product(id=8, name="earpod", description="budget earpod budget", price=1000, quantity=14),
    Product(id=9, name="speeker", description="boat speeker budget", price=1000, quantity=21)
]

@app.get("/product")
async def get_all_product():
    return products

from models import Product
@app.post("/product")
async def add_a_product(product:Product):
    products.append(product)
    return product

@app.put("/product/{id}")
async def update_a_product(id:int,product:Product):
    for i in range(len(products)):
        if products[i].id==id:
            products[i]=product
            return "Product added successfully"
    return "No product found"

@app.delete("/product/{id}")
async def delete_a_product(id:int):
    for i in range(len(products)):
        if products[i].id ==id:
            del products[i]
            return "product deleted"
    return "No product found"

@app.get("/product/search/{word}")
async def get_products_by_name_keyword(word:str):
    results=[]
    # for product in products:
    #     if product.name.lower() == name.lower():
    #         return product
    for product in products:
        if word.lower() in product.name.lower():
            results.append(product)
    if results:
        return results
    return {"message": "No product found"}

# @app.get("/product/{user_entered_price}")
# async def get_product_by_price_filter(user_entered_price:float):
#     result=[]
#     for product in products:
#         if user_entered_price <= 500:
#             return product for product.price < 500
#         if user_entered_price <= 1000:
#             return product for product.price < 1000


@app.get("/product/price/{user_entered_max_price}")
async def get_product_by_price_filter(user_entered_max_price: float):
    if user_entered_max_price <= 500:
        return [p for p in products if p.price < 500]
    elif user_entered_max_price <= 1000:
        return [p for p in products if p.price < 1000]
    elif user_entered_max_price <= 5000:
        return [p for p in products if p.price < 5000]
    elif user_entered_max_price <= 10000:
        return [p for p in products if p.price < 10000]
    elif user_entered_max_price <= 20000:
        return [p for p in products if p.price < 20000]
    elif user_entered_max_price <= 50000:
        return [p for p in products if p.price < 50000]
    else:
        return {"message": "No products found in this range"}

@app.get("/product/filter/{word}/{max_price}")
async def get_product_by_name_and_price(word: str, max_price: float):
    results = [
        p for p in products
        if word.lower() in p.name.lower() and p.price <= max_price
    ]
    if results:
        return results
    return {"message": "No products found"}

# @app.get("/product/filter/{word}/{max_price}")
# async def get_product_by_name_and_price(word: str, max_price: float):
#     results = [
#         p for p in products
#         if word.lower() in p.name.lower() and p.price <= max_price
#     ]
#     if results:
#         return results
#     return {"message": "No products found"}
