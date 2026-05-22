from pydantic import BaseModel
from typing import Optional
from datetime import date


class CustomerCreate(BaseModel):
    register_customer_number: int
    customer_name: str
    address: str
    customer_type: bool


class ProductCreate(BaseModel):
    barcode: int
    product_name: str
    category: int
    batch_number: int
    expiration_date: date
    price: float


class OrderCreate(BaseModel):
    order_number: int
    order_date: date
    amount: int
    barcode: int
    register_customer_number: int


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    address: Optional[str] = None
    customer_type: Optional[bool] = None


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[int] = None
    batch_number: Optional[int] = None
    expiration_date: Optional[date] = None
    price: Optional[float] = None


class OrderUpdate(BaseModel):
    amount: Optional[int] = None
    barcode: Optional[int] = None
    register_customer_number: Optional[int] = None


class CustomerResponse(BaseModel):
    register_customer_number: int
    customer_name: str
    address: str
    customer_type: bool

    model_config = {
        "from_attributes": True
    }


class ProductResponse(BaseModel):
    barcode: int
    product_name: str
    category: int
    batch_number: int
    expiration_date: date
    price: float

    model_config = {
        "from_attributes": True
    }


class OrderResponse(BaseModel):
    order_number: int
    order_date: date
    amount: int
    barcode: int
    register_customer_number: int

    model_config = {
        "from_attributes": True
    }
