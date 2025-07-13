from typing import List, Optional
from datetime import timedelta
from fastapi import APIRouter, status, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from . import crud
from . import auth
from .schemas import (
    TransferCreate, TransferPublic, TransferUpdate, Token, UserInDB, TransferStatus, UserCreate, UserPublic
)
from .dependencies import get_current_user, get_db
from .config import settings
from .database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

# --- Роутер для аутентификации ---
auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database(request.app)
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(request: Request, user_data: UserCreate):
    """
    Временный эндпоинт для создания пользователя.
    """
    db = get_database(request.app)
    try:
        created_user = await crud.create_user(db, user_data)
        return UserPublic(
            _id=created_user.id,
            username=created_user.username
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# --- Роутер для трансферов (теперь защищенный) ---
router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=TransferPublic, status_code=status.HTTP_201_CREATED)
async def create_new_transfer(transfer: TransferCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud.create_transfer(db=db, transfer_data=transfer)

@router.get("/", response_model=List[TransferPublic])
async def read_transfers(db: AsyncIOMotorDatabase = Depends(get_db), status: Optional[TransferStatus] = None):
    return await crud.get_transfers(db=db, status=status)

@router.get("/{transfer_id}", response_model=TransferPublic)
async def read_single_transfer(transfer_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    db_transfer = await crud.get_transfer_by_id(db, transfer_id)
    if db_transfer is None:
        raise HTTPException(status_code=404, detail="Трансфер не найден")
    return db_transfer

@router.patch("/{transfer_id}", response_model=TransferPublic)
async def update_single_transfer(transfer_id: str, transfer_update: TransferUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    updated_transfer = await crud.update_transfer_by_id(db, transfer_id, transfer_update)
    if updated_transfer is None:
        raise HTTPException(status_code=404, detail="Трансфер не найден")
    return updated_transfer

@router.delete("/{transfer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_transfer(transfer_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    was_deleted = await crud.delete_transfer_by_id(db, transfer_id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Трансфер не найден")
    return Response(status_code=status.HTTP_204_NO_CONTENT) 