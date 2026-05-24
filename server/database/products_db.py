from sqlalchemy import ClauseElement, select, insert, update, delete

from .models import Products, DataBase


class ProductsDB(DataBase):
    @staticmethod
    def select_all() -> ClauseElement:
        return select(Products)

    @staticmethod
    def select_by_id(barcode: int) -> ClauseElement:
        return select(Products).where(Products.barcode == barcode)

    @classmethod
    def insert_by_id(cls, barcode: int, **kwargs) -> ClauseElement:
        return insert(Products).values(barcode=barcode, **kwargs)

    @classmethod
    def update_by_id(cls, barcode: int, **kwargs) -> ClauseElement:
        return update(Products).where(Products.barcode == barcode).values(**kwargs)

    @staticmethod
    def delete_by_id(barcode: int) -> ClauseElement:
        return delete(Products).where(Products.barcode == barcode)