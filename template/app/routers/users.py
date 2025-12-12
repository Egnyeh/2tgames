from fastapi import APIRouter, Depends, Header, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserOut, UserDb, UserCreate
from app.auth.auth import (
    TokenData,
    create_access_token,
    Token,
    verify_password,
    oauth2_scheme,
    decode_token,
)
from app.database import get_user_by_username, insert_user, get_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    userDb = get_user_by_username(user.username)
    if userDb is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )

    user_id = insert_user(user)

    created_user = get_user_by_id(user_id)

    return UserOut(
        id=created_user.id,
        email=created_user.email,
        username=created_user.username,
        nombre=created_user.nombre,
        tipo=created_user.tipo,
    )


@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Buscamos username y password en la petición HTTP
    username: str | None = form_data.username
    password: str | None = form_data.password

    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect",
        )

    # 2. Buscamos username en la bbdd
    userFound = get_user_by_username(username)
    if not userFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect",
        )

    # 3. Checkeamos contraseñas
    user: UserDb = userFound[0]
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect",
        )

    token_data = {"user_id": user.id, "username": user.username, "tipo": user.tipo}


    access_token = create_access_token(token_data)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)

    user = get_user_by_id(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserOut(
        id=user.id,
        email=user.email,
        username=user.username,
        nombre=user.nombre,
        tipo=user.tipo,
    )
