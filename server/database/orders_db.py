from sqlalchemy import ClauseElement, select, insert, update, delete
from datetime import date

from .models import Orders, DataBase


class OrdersDB(DataBase):
    correct_types = {
        'order_number': lambda x: isinstance(x, int) and 0 < x < 10**10,
        'order_date': lambda x: isinstance(x, date),
        'barcode ': lambda x: isinstance(x, int) and 0 < x < 10 ** 13,
        'amount': lambda x: isinstance(x, int) and 0 < x < 10**9,
        'register_customer_number': lambda x: isinstance(x, int) and 0 < x < 10**11,
    }

    @staticmethod
    def select_all() -> ClauseElement:
        return select(Orders)

    @staticmethod
    def select_by_id(order_number: int, order_date: date) -> ClauseElement:
        return select(Orders).where(Orders.order_number == order_number, Orders.order_date == order_date)

    @classmethod
    def insert_by_id(cls, order_number: int, order_date: date, **kwargs) -> ClauseElement:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при добавлении строки в базу данных')

        return insert(Orders).values(order_number=order_number, order_date=order_date, **kwargs)

    @classmethod
    def update_by_id(cls, order_number: int, order_date: date, **kwargs) -> ClauseElement:
        for key, value in kwargs.items():
            if not cls.correct_types[key](value):
                raise Exception('Неверные данные при обновлении строки в базе данных')

        return update(Orders).where(Orders.barcode == order_number, Orders.order_date == order_date).values(**kwargs)

    @staticmethod
    def delete_by_id(order_number: int, order_date: date) -> ClauseElement:
        return delete(Orders).where(Orders.order_number == order_number, Orders.order_date == order_date)
