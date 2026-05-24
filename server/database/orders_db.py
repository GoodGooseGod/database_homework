from sqlalchemy import ClauseElement, select, insert, update, delete
from datetime import date

from .models import Orders, DataBase


class OrdersDB(DataBase):
    @staticmethod
    def select_all() -> ClauseElement:
        return select(Orders)

    @staticmethod
    def select_by_id(order_number: int, order_date: date) -> ClauseElement:
        return select(Orders).where(Orders.order_number == order_number, Orders.order_date == order_date)

    @classmethod
    def insert_by_id(cls, order_number: int, order_date: date, **kwargs) -> ClauseElement:
        return insert(Orders).values(order_number=order_number, order_date=order_date, **kwargs)

    @classmethod
    def update_by_id(cls, order_number: int, order_date: date, **kwargs) -> ClauseElement:
        return update(Orders).where(Orders.order_number == order_number, Orders.order_date == order_date).values(**kwargs)

    @staticmethod
    def delete_by_id(order_number: int, order_date: date) -> ClauseElement:
        return delete(Orders).where(Orders.order_number == order_number, Orders.order_date == order_date)
