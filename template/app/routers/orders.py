from operator import add
from venv import create
from webbrowser import get
from fastapi import APIRouter, Depends, status, HTTPException

from app.models import OrderCreate, OrderOut, ProductOut, TokenData, ProductInOrder
from app.auth.auth import get_current_user
from app.database import get_order_lines, create_order_with_items, get_order_lines, get_orders_by_user, get_product_by_id
from app.routers import products

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
    #Primero miramos que el pedido tenga lineas
    if not order_data.lineas or len(order_data.lineas) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El pedido debe contener al menos una linea"
        )
    #Ahora validamos que los productos y existan y calculamos el precio total
    total_price = 0.0
    items_to_insert = []

    for linea in order_data.lineas:
        #Obtenemos el producto con ese id de la base de datos
        producto = get_product_by_id(linea.id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con id {linea.id} no existe"
            )
        if not producto.disponibilidad or producto.stock < linea.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto con id {linea.id} no tiene stock suficiente"
            )
        
        #Calculamos el precio total de cada linea
        linea_price = producto.precio_unitario * linea.cantidad
        total_price += linea_price

        # Preparamos el objeto item para insertar
        items_to_insert.append({
            "id_producto": linea.id,
            "cantidad": linea.cantidad,
            "precio": producto.precio_unitario
        })

        #Creamos el pedido en la base de datos
        from datetime import date

        order_dict = {
            "id_usuario": user.user_id,
            "fecha_pedido": date.today(),
            "precio_total": total_price,
            "estado": 1 #Estado 1: Pendiente
        }

        numero_pedido = create_order_with_items(order_dict, items_to_insert)

        if not numero_pedido:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el pedido"
            )
        
        #Finalmente, devolvemos el pedido creado
        lineas_insertadas = get_order_lines(numero_pedido)

        return OrderOut(
            numero_pedido=numero_pedido,
            id_usuario=user.user_id,
            fecha_pedido=date.today(),
            precio_total=total_price,
            estado=1,
            lineas=lineas_insertadas
        )


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