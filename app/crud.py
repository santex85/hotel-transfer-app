from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from .schemas import TransferCreate, TransferStatus, TransferPublic

# Название коллекции в MongoDB
COLLECTION_NAME = "transfers"

async def create_transfer(db: AsyncIOMotorDatabase, transfer_data: TransferCreate) -> TransferPublic:
    """
    Сохраняет новый документ трансфера в базе данных.

    :param db: Экземпляр базы данных MongoDB
    :param transfer_data: Pydantic-модель с данными для нового трансфера.
    :return: TransferPublic модель с данными созданного трансфера.
    """
    collection = db[COLLECTION_NAME]

    # Преобразуем Pydantic модель в словарь
    transfer_dict = transfer_data.model_dump()

    # Добавляем поля со значениями по умолчанию
    transfer_dict["status"] = TransferStatus.SCHEDULED.value
    
    # Вставляем документ в коллекцию
    result = await collection.insert_one(transfer_dict)
    
    # Создаем и возвращаем TransferPublic модель
    return TransferPublic(
        _id=str(result.inserted_id),
        status=TransferStatus.SCHEDULED,
        **transfer_data.model_dump()
    )

async def get_transfers(db: AsyncIOMotorDatabase, status: Optional[TransferStatus] = None) -> List[dict]:
    """
    Извлекает список документов трансфера из базы данных.

    :param db: Экземпляр базы данных MongoDB
    :param status: Опциональный фильтр по статусу трансфера.
    :return: Список словарей с данными трансферов.
    """
    collection = db[COLLECTION_NAME]
    
    query = {}
    if status:
        query["status"] = status.value
    
    cursor = collection.find(query)
    
    # Собираем все документы из курсора в список
    transfers = await cursor.to_list(length=100) # Ограничим выборку 100 записями
    
    # Преобразуем ObjectId в строки для корректной сериализации
    for transfer in transfers:
        if "_id" in transfer:
            transfer["_id"] = str(transfer["_id"])
    
    return transfers 