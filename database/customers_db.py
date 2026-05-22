from sqlalchemy import ClauseElement, select, insert, update, delete

from .models import Customers, DataBase


class CustomersDB(DataBase):
    correct_types = {
        'register_customer_number': lambda x: isinstance(x, int) and 0 < x < 10**11,
        'customer_name': lambda x: isinstance(x, str) and len(x) <= 30,
        'address': lambda x: isinstance(x, str) and len(x) <= 40,
        'customer_type': lambda x: isinstance(x, bool),
    }

    @staticmethod
    def select_all() -> ClauseElement:
        return select(Customers)

    @staticmethod
    def select_by_id(register_customer_number: int, order_date=None) -> ClauseElement:
        return select(Customers).where(Customers.register_customer_number == register_customer_number)

    @classmethod
    def insert_by_id(cls, register_customer_number: int, order_date=None, **kwargs) -> ClauseElement:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при добавлении строки в базу данных')

        if kwargs.get('register_customer_number'):
            register_customer_number = kwargs.get('register_customer_number')

        return insert(Customers).values(register_customer_number=register_customer_number, **kwargs)

    @classmethod
    def update_by_id(cls, register_customer_number: int, order_date=None, **kwargs) -> ClauseElement:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при обновлении строки в базе данных')

        if kwargs.get('register_customer_number'):
            register_customer_number = kwargs.get('register_customer_number')
        return update(Customers).where(Customers.register_customer_number == register_customer_number).values(**kwargs)

    @staticmethod
    def delete_by_id(register_customer_number: int, order_date=None) -> ClauseElement:
        return delete(Customers).where(Customers.register_customer_number == register_customer_number)