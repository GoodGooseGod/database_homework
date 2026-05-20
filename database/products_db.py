from sqlalchemy import Select, Insert, Delete, Update, select, insert, update, delete
from datetime import date

from .models import Products, DataBase


class ProductsDB(DataBase):
    correct_types = {
        'id': lambda x: isinstance(x, int) and 0 < x < 10 ** 13,
        'barcode ': lambda x: isinstance(x, int) and 0 < x < 10 ** 13,
        'product_name': lambda x: isinstance(x, str) and len(x) <= 30,
        'category': lambda x: isinstance(x, int) and 0 <= x < 10,
        'batch_number': lambda x: isinstance(x, int) and 0 <= x < 10**3,
        'expiration_date': lambda x: isinstance(x, date),
        'price': lambda x: isinstance(x, float) and x >= 0,
    }

    @staticmethod
    def select_all() -> Select:
        return select(Products)

    @staticmethod
    def select_by_id(id: int, order_date=None) -> Select:
        return select(Products).where(Products.barcode == id)

    @classmethod
    def insert_by_id(cls, id: int, order_date=None, **kwargs) -> Insert:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при добавлении строки в базу данных')

        if kwargs.get('barcode'):
            id = kwargs.get('barcode')

        return insert(Products).values(barcode=id, **kwargs)

    @classmethod
    def update_by_id(cls, id: int, order_date=None, **kwargs) -> Update:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при обновлении строки в базе данных')

        if kwargs.get('barcode'):
            id = kwargs.get('barcode')

        return update(Products).where(Products.barcode == id).values(**kwargs)

    @staticmethod
    def delete_by_id(id: int, order_date=None) -> Delete:
        return delete(Products).where(Products.barcode == id)