from fastapi import APIRouter, status, Request, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from . import crud
from .schemas import TransferCreate, TransferPublic, TransferStatus
from .database import get_database

# Создаем новый роутер для эндпоинтов, связанных с трансферами
router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
)

async def get_db(request: Request) -> AsyncIOMotorDatabase:
    """
    Зависимость для получения экземпляра базы данных.
    """
    return get_database(request.app)

@router.post("/", response_model=TransferPublic, status_code=status.HTTP_201_CREATED)
async def create_new_transfer(
    transfer: TransferCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Создает новую запись о трансфере.
    """
    created_transfer = await crud.create_transfer(db=db, transfer_data=transfer)
    return created_transfer

@router.get("/", response_model=List[TransferPublic])
async def read_transfers(
    status: Optional[TransferStatus] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Возвращает список трансферов.
    Можно отфильтровать по статусу (scheduled, completed, canceled).
    """
    return await crud.get_transfers(db=db, status=status) 