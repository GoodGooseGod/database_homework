from fastapi import APIRouter, HTTPException


from .schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)


def products_router(db_manager) -> APIRouter:
    router = APIRouter(
        prefix='/products',
        tags=['Products']
    )


    @router.get('/', response_model=list[ProductResponse])
    async def get_products() -> list[ProductResponse]:
        return await db_manager.get_all('products')


    @router.get('/{barcode}', response_model=ProductResponse)
    async def get_product_by_barcode(barcode: int) -> ProductResponse:
        product = await db_manager.get_one(
            'products',
            barcode
        )

        if product is None:
            raise HTTPException(status_code=404, detail='Product not found')
        return product


    @router.post('/', response_model=ProductResponse, status_code=201)
    async def create_product(product: ProductCreate) -> ProductResponse:
        await db_manager.put(
            'products',
            id=product.barcode,
            **product.model_dump()
        )
        created_product = await db_manager.get_one(
            'products',
            product.barcode
        )

        return created_product


    @router.put('/{barcode}', response_model=ProductResponse)
    async def update_product(barcode: int, product: ProductUpdate) -> ProductResponse:
        existing_product = await db_manager.get_one(
            'products',
            barcode
        )

        if existing_product is None:
            raise HTTPException(
                status_code=404,
                detail='Product not found'
            )

        await db_manager.update(
            'products',
            id=barcode,
            **product.model_dump(exclude_unset=True)
        )
        updated_product = await db_manager.get_one(
            'products',
            barcode
        )
        return updated_product


    @router.delete('/{barcode}', status_code=204)
    async def delete_product(barcode: int):
        existing_product = await db_manager.get_one(
            'products',
            barcode
        )

        if existing_product is None:
            raise HTTPException(
                status_code=404,
                detail='Product not found'
            )

        await db_manager.delete(
            'products',
            id=barcode
        )

    return router
