from fastapi import APIRouter, Depends, status, HTTPException
from datetime import date

from app.auth.auth import oauth2_scheme, decode_token, TokenData
from app.database import (
    create_order_with_items,
    get_product_by_id,
    get_user_by_username
)
from app.models import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    token: str = Depends(oauth2_scheme)
):
    #Validar token
    data: TokenData = decode_token(token)

    if data.username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    #Obtener usuario
    user = get_user_by_username(data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not order.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one product"
        )

    #Validar productos y calcular precio total
    total_price = 0
    items_db = []

    for item in order.items:
        product = get_product_by_id(item.id_producto)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.id_producto} not found"
            )

        if item.cantidad <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero"
            )

        total_price += product.precio_unitario * item.cantidad

        items_db.append({
            "id_producto": item.id_producto,
            "cantidad": item.cantidad,
            "precio": product.precio_unitario
        })

    #Crear pedido
    pedido_db = {
        "id_usuario": user.id,
        "fecha_pedido": date.today(),
        "precio_total": total_price,
        "estado": "CREADO"
    }

    numero_pedido = create_order_with_items(pedido_db, items_db)

    if numero_pedido is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/", response_model=list[OrderOut], status_code=status.HTTP_200_OK)
async def get_all_orders(user: TokenData = Depends(get_current_user)):
    orders = get_orders_by_user(user.id_usuario)
    return orders


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
 