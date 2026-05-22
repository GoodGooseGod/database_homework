from fastapi import APIRouter, HTTPException


from api_manager import db_manager
from .schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)

router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)


@router.get("/")
async def get_products():
    return await db_manager.get_all('customers')


@router.post("/")
async def create_product(customer: CustomerCreate):
    await db_manager.put(
        'customers',
        id=customer.register_customer_number,
        **customer.model_dump()
    )