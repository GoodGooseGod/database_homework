from sqlalchemy import Select, Insert, Delete, Update, select, insert, update, delete

from .models import Customers, DataBase


class CustomersDB(DataBase):
    correct_types = {
        'id': lambda x: isinstance(x, int) and 0 < x < 10**11,
        'register_customer_number': lambda x: isinstance(x, int) and 0 < x < 10**11,
        'name': lambda x: isinstance(x, str) and len(x) <= 30,
        'address': lambda x: isinstance(x, str) and len(x) <= 40,
        'customer_type': lambda x: isinstance(x, bool),
    }

    @staticmethod
    def select_all() -> Select:
        return select(Customers)

    @staticmethod
    def select_by_id(id: int, order_date=None) -> Select:
        return select(Customers).where(Customers.register_customer_number == id)

    @classmethod
    def insert_by_id(cls, id: int, order_date=None, **kwargs) -> Insert:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при добавлении строки в базу данных')

        if kwargs.get('register_customer_number'):
            id = kwargs.get('register_customer_number')

        return insert(Customers).values(register_customer_number=id, **kwargs)

    @classmethod
    def update_by_id(cls, id: int, order_date=None, **kwargs) -> Update:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при обновлении строки в базе данных')

        if kwargs.get('register_customer_number'):
            id = kwargs.get('register_customer_number')
        return update(Customers).where(Customers.register_customer_number == id).values(**kwargs)

    @staticmethod
    def delete_by_id(id: int, order_date=None) -> Delete:
        return delete(Customers).where(Customers.register_customer_number == id)