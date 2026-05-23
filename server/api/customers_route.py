from fastapi import APIRouter, HTTPException


from .schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)


def customers_router(db_manager) -> APIRouter:
    router = APIRouter(
        prefix='/customers',
        tags=['Customers']
    )


    @router.get('/', response_model=list[CustomerResponse])
    async def get_customers() -> list[CustomerResponse]:
        return await db_manager.get_all('customers')


    @router.get('/{register_customer_number}', response_model=CustomerResponse)
    async def get_customer_by_reg_num(register_customer_number: int) -> CustomerResponse:
        customer = await db_manager.get_one(
            'customers',
            register_customer_number
        )

        if customer is None:
            raise HTTPException(status_code=404, detail='Customer not found')
        return customer


    @router.post('/', response_model=CustomerResponse, status_code=201)
    async def create_customer(customer: CustomerCreate) -> CustomerResponse:
        await db_manager.put(
            'customers',
            id=customer.register_customer_number,
            **customer.model_dump()
        )
        created_customer = await db_manager.get_one(
            'customers',
            customer.register_customer_number
        )

        return created_customer


    @router.put('/{register_customer_number}', response_model=CustomerResponse)
    async def update_customer(register_customer_number: int, customer: CustomerUpdate) -> CustomerResponse:
        existing_customer = await db_manager.get_one(
            'customers',
            register_customer_number
        )

        if existing_customer is None:
            raise HTTPException(
                status_code=404,
                detail='Customer not found'
            )

        await db_manager.update(
            'customers',
            id=register_customer_number,
            **customer.model_dump(exclude_unset=True)
        )
        updated_customer = await db_manager.get_one(
            'customers',
            register_customer_number
        )
        return updated_customer


    @router.delete('/{register_customer_number}', status_code=204)
    async def delete_customer(register_customer_number: int):
        existing_customer = await db_manager.get_one(
            'customers',
            register_customer_number
        )

        if existing_customer is None:
            raise HTTPException(
                status_code=404,
                detail='Customer not found'
            )

        await db_manager.delete(
            'customers',
            id=register_customer_number
        )

    return router
