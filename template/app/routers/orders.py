from venv import create
from fastapi import APIRouter, Depends, status, HTTPException

from app.models import OrderCreate, OrderOut, ProductOut, TokenData, ProductInOrder
from app.auth.auth import get_current_user
from app.database import add_product_to_order, create_order_with_items, get_orders_by_user
from template.app.routers import products

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderOut], status_code=status.HTTP_200_OK)
async def get_all_orders(user: TokenData = Depends(get_current_user)):
    orders = get_orders_by_user(user.id_usuario)
    return orders

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    user: TokenData = Depends(get_current_user)
):
    try:
        new_order = create_order_with_items(
            order=order_data,
            items=[
                ProductInOrder(
                    id=line.id_producto, 
                    cantidad=line.cantidad
                ) 
                for line in order_data.lineas
            ]
        )
        return new_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

"""
@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_new_order(
    order: OrderCreate,
    user: TokenData = Depends(get_current_user)
):
    try:
        order_id = create_order_with_items(user.id_usuario, order)

        orders = get_orders_by_user(user.id_usuario)
        created_order = next((o for o in orders), None)

        if not created_order:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al obtener el pedido creado"
            )
        return created_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
"""

"""
@router.get("/{order_id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
async def get_order_by_user(
    order_id: int,
    user: TokenData = Depends(get_current_user)
):
    orders = get_orders_by_user(user.id_usuario)
    order = next((o for o in orders), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
"""