from sqlalchemy.ext.asyncio import async_sessionmaker, engine
from datetime import date


from models import DataBase
from .customers_db import CustomersDB
from .products_db import  ProductsDB
from .orders_db import OrdersDB


class DatabaseManager:
    def __init__(self, db_engine: engine):
        self.customers = CustomersDB
        self.products = ProductsDB
        self.orders = OrdersDB

        self.session_maker = async_sessionmaker(bind=db_engine)

    def select_db(self, database: str) -> DataBase:
        if database == 'customers':
            return self.customers
        if database == 'products':
            return self.products
        if database == 'orders':
            return self.orders
        raise Exception('Выбрана неверная база данных!')

    async def get_all(self, database: str):
        db = self.select_db(database)
        async with self.session_maker() as session:
            stmt = db.select_all()
            res = await session.execute(stmt)
            return res.scalars().all()

    async def get_one(self, database: str, id: int, order_date: date = None):
        db = self.select_db(database)
        async with self.session_maker() as session:
            if order_date is None:
                stmt = db.select_by_id(id)
            else:
                stmt = db.select_by_id(id, order_date)

            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def put(self, database: str, **kwargs):
        db = self.select_db(database)
        async with self.session_maker() as session:
            stmt = db.insert_by_id(**kwargs)
            res = await session.execute(stmt)
            await session.commit()
            return res

    async def update(self, database: str, **kwargs):
        db = self.select_db(database)
        async with self.session_maker() as session:
            stmt = db.update_by_id(**kwargs)
            res = await session.execute(stmt)
            await session.commit()
            return res

    async def delete(self, database: str, **kwargs):
        db = self.select_db(database)
        async with self.session_maker() as session:
            stmt = db.delete_by_id(**kwargs)
            res = await session.execute(stmt)
            await session.commit()
            return res
