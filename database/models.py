from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, VARCHAR, Float, Date, ClauseElement
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, MEDIUMINT
from sqlalchemy.sql import Select
from sqlalchemy.sql.dml import Insert, Update, Delete
from datetime import date
from typing import Protocol


class Base(DeclarativeBase):
    pass


class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    register_customer_number: Mapped[int] = mapped_column(INTEGER(11, unsigned=True), primary_key=True)
    customer_name: Mapped[str] = mapped_column(VARCHAR(30))
    address: Mapped[str] = mapped_column(VARCHAR(40))
    customer_type: Mapped[bool] = mapped_column(TINYINT(1))


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci"
    }

    barcode: Mapped[int] = mapped_column(INTEGER(13, unsigned=True), primary_key=True)
    product_name: Mapped[str] = mapped_column(VARCHAR(30))
    category: Mapped[int] = mapped_column(TINYINT(1, unsigned=True))
    batch_number: Mapped[int] = mapped_column(TINYINT(3, unsigned=True))
    expiration_date: Mapped[date] = mapped_column(Date)
    price: Mapped[float] = mapped_column(Float)


class Orders(Base):
    __tablename__ = 'orders'

    order_number: Mapped[int] = mapped_column(INTEGER(10, unsigned=True), primary_key=True)
    order_date: Mapped[date] = mapped_column(Date, primary_key=True)
    amount: Mapped[int] = mapped_column(MEDIUMINT(9))
    barcode: Mapped[int] = mapped_column(
        INTEGER(13, unsigned=True),
        ForeignKey('products.barcode')
    )
    register_customer_number: Mapped[int] = mapped_column(
        INTEGER(11, unsigned=True),
        ForeignKey('customers.register_customer_number')
    )


class DataBase(Protocol):
    @staticmethod
    def select_all() -> Select:
        ...

    @staticmethod
    def select_by_id(*args, **kwargs) -> Select:
        ...

    @classmethod
    def insert_by_id(cls, **kwargs) -> Insert:
        ...

    @classmethod
    def update_by_id(cls, **kwargs) -> Update:
        ...

    @staticmethod
    def delete_by_id(*args, **kwargs) -> Delete:
        ...
