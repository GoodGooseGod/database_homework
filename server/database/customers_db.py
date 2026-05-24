from sqlalchemy import ClauseElement, select, insert, update, delete

from .models import Customers, DataBase


class CustomersDB(DataBase):
    @staticmethod
    def select_all() -> ClauseElement:
        return select(Customers)

    @staticmethod
    def select_by_id(register_customer_number: int) -> ClauseElement:
        return select(Customers).where(Customers.register_customer_number == register_customer_number)

    @classmethod
    def insert_by_id(cls, register_customer_number: int, **kwargs) -> ClauseElement:
        return insert(Customers).values(register_customer_number=register_customer_number, **kwargs)

    @classmethod
    def update_by_id(cls, register_customer_number: int, **kwargs) -> ClauseElement:
        return update(Customers).where(Customers.register_customer_number == register_customer_number).values(**kwargs)

    @staticmethod
    def delete_by_id(register_customer_number: int) -> ClauseElement:
        return delete(Customers).where(Customers.register_customer_number == register_customer_number)