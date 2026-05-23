from fastapi import APIRouter, HTTPException
from datetime import date


from .schemas import (
    OrderCreate,
    OrderUpdate,
    OrderResponse
)


def orders_router(db_manager) -> APIRouter:
    router = APIRouter(
        prefix='/orders',
        tags=['Orders']
    )


    @router.get('/', response_model=list[OrderResponse])
    async def get_orders() -> list[OrderResponse]:
        return await db_manager.get_all('orders')


    @router.get('/{order_number}/{order_date}', response_model=OrderResponse)
    async def get_order_by_num_and_date(order_number: int, order_date: date) -> OrderResponse:
        order = await db_manager.get_one(
            'orders',
            order_number,
            order_date
        )

        if order is None:
            raise HTTPException(status_code=404, detail='Order not found')
        return order


    @router.post('/', response_model=OrderResponse, status_code=201)
    async def create_order(order: OrderCreate) -> OrderResponse:
        await db_manager.put(
            'orders',
            id=order.order_number,
            order_date=order.order_date,
            **order.model_dump()
        )
        created_order = await db_manager.get_one(
            'orders',
            order.order_number,
            order.order_date,
        )

        return created_order


    @router.put('/{order_number}/{order_date}', response_model=OrderResponse)
    async def update_order(order_number: int, order_date: date, order: OrderUpdate) -> OrderResponse:
        existing_order = await db_manager.get_one(
            'orders',
            order_number,
            order_date
        )

        if existing_order is None:
            raise HTTPException(
                status_code=404,
                detail='Order not found'
            )

        await db_manager.update(
            'orders',
            id=order_number,
            order_date=order_date,
            **order.model_dump(exclude_unset=True)
        )
        updated_order = await db_manager.get_one(
            'orders',
            order_number,
            order_date,
        )
        return updated_order


    @router.delete('/{order_number}/{order_date}', status_code=204)
    async def delete_order(order_number: int, order_date: date):
        existing_order = await db_manager.get_one(
            'orders',
            order_number,
            order_date,
        )

        if existing_order is None:
            raise HTTPException(
                status_code=404,
                detail='Order not found'
            )

        await db_manager.delete(
            'orders',
            id=order_number,
            order_date=order_date,
        )

    return router
