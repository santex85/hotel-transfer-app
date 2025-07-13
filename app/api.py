from fastapi import APIRouter, status, Request, Depends, HTTPException, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from . import crud
from .schemas import TransferCreate, TransferPublic, TransferStatus, TransferUpdate
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

@router.get("/{transfer_id}", response_model=TransferPublic)
async def read_single_transfer(
    transfer_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Возвращает один трансфер по ID.
    """
    db_transfer = await crud.get_transfer_by_id(db, transfer_id)
    if db_transfer is None:
        raise HTTPException(status_code=404, detail="Трансфер не найден")
    return db_transfer

@router.patch("/{transfer_id}", response_model=TransferPublic)
async def update_single_transfer(
    transfer_id: str,
    transfer_update: TransferUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Частично обновляет данные трансфера.
    """
    updated_transfer = await crud.update_transfer_by_id(db, transfer_id, transfer_update)
    if updated_transfer is None:
        raise HTTPException(status_code=404, detail="Трансфер не найден или нет данных для обновления")
    return updated_transfer

@router.delete("/{transfer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_transfer(
    transfer_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Удаляет трансфер по ID.
    """
    was_deleted = await crud.delete_transfer_by_id(db, transfer_id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Трансфер не найден")
    return Response(status_code=status.HTTP_204_NO_CONTENT) 