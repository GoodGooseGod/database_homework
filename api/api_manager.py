from fastapi import FastAPI

from api.customers_route import router as customer_router
from api.products_route import router as products_router
from api.orders_route import router as orders_router


api = FastAPI()
api.include_router(customer_router)
api.include_router(products_router)
api.include_router(orders_router)

