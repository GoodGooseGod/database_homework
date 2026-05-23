from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
import uvicorn

from database.database_manager import DatabaseManager
from api.customers_route import customers_router
from api.products_route import products_router
from api.orders_route import orders_router


class App:
    def __init__(self, db_path):
        self.engine = create_async_engine(db_path)
        self.db = DatabaseManager(self.engine)
        self.api = FastAPI()
        self.include_routes()

    def include_routes(self) -> None:
        self.api.include_router(customers_router(self.db))
        self.api.include_router(products_router(self.db))
        self.api.include_router(orders_router(self.db))

    def run(self) -> None:
        uvicorn.run(self.api)

