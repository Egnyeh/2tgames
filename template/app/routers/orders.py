from fastapi import APIRouter, Depends, status, HTTPException

from app.models import OrderCreate, OrderOut, TokenData
from app.auth.auth import get_current_user
from app.database import create_order, get_orders_by_user

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_new_order(
    order: OrderCreate,
    user: TokenData = Depends(get_current_user)
):
    try:
        order_id = create_order(user.user_id, order)

        orders = get_orders_by_user(user.user_id)
        created_order = next((o for o in orders if o.order_number == order_id), None)

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


@router.get("/", response_model=list[OrderOut], status_code=status.HTTP_200_OK)
async def get_all_orders(user: TokenData = Depends(get_current_user)):
    orders = get_orders_by_user(user.user_id)
    return orders


@router.get("/{order_id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
async def get_order_by_user(
    order_id: int,
    user: TokenData = Depends(get_current_user)
):
    orders = get_orders_by_user(user.user_id)
    order = next((o for o in orders if o.order_number == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
 