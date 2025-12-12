from math import prod
from fastapi import APIRouter, Depends, status, HTTPException

from app.models import ProductCreate, ProductUpdate, ProductOut, TokenData
from app.auth.auth import oauth2_scheme, decode_token, verify_admin
from app.database import (
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product
)

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[ProductOut], status_code=status.HTTP_200_OK)
async def get_products():
    products = get_all_products()
    return products


@router.get("/{product_id}/", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get_product(product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    admin: TokenData = Depends(verify_admin) 
):
    existing_product = get_product_by_id(product_id)
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    success = update_product(product_id, product)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update product")

    updated_product = get_product_by_id(product_id)
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    admin: TokenData = Depends(verify_admin)
):
    existing_product = get_product_by_id(product_id)
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    success = delete_product(product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete product")
    return None