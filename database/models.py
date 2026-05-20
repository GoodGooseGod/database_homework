from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, ForeignKey, Boolean, VARCHAR, Float, Date
from sqlalchemy import Select, Insert, Update, Delete
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, MEDIUMINT
from datetime import date
from typing import Protocol


class Base(DeclarativeBase):
    pass


class Customers(Base):
    __tablename__ = 'customers'

    register_customer_number: int = Column(INTEGER(display_width=11), primary_key=True, unsigned=True)
    name: str = Column(VARCHAR(30), mysql_charset='utf8mb4', mysql_collate='utf8mb4_general_ci')
    address: str = Column(VARCHAR(40), mysql_charset='utf8mb4', mysql_collate='utf8mb4_general_ci')
    customer_type: bool = Column(Boolean)


class Products(Base):
    __tablename__ = 'products'

    barcode: int = Column(INTEGER(display_width=13), primary_key=True, unsigned=True)
    product_name: str = Column(VARCHAR(30), mysql_charset='utf8mb4', mysql_collate='utf8mb4_general_ci')
    category: int = Column(TINYINT(display_width=1), unsigned=True)
    batch_number: int = Column(TINYINT(display_width=3), unsigned=True)
    expiration_date: date = Column(Date)
    price: float = Column(Float)


class Orders(Base):
    __tablename__ = 'orders'

    order_number: int = Column(INTEGER(display_width=10), primary_key=True, unsigned=True)
    order_date: date = Column(Date, primary_key=True)
    barcode: int = Column(ForeignKey('products.barcode'), unsigned=True)
    amount: int = Column(MEDIUMINT(display_width=9))
    register_customer_number: int = Column(ForeignKey('customers.register_customer_number'), unsigned=True)


class DataBase(Protocol):
    @staticmethod
    def select_all() -> Select:
        pass

    @staticmethod
    def select_by_id(id: int, order_date: date) -> Select:
        pass

    @classmethod
    def insert_by_id(cls, id: int, order_date: date, **kwargs) -> Insert:
        pass

    @classmethod
    def update_by_id(cls, id: int, order_date: date, **kwargs) -> Update:
        pass

    @staticmethod
    def delete_by_id(id: int, order_date: date) -> Delete:
        pass
