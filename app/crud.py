from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from .database import get_database
from .schemas import TransferCreate, TransferStatus

# Название коллекции в MongoDB
COLLECTION_NAME = "transfers"

async def create_transfer(transfer_data: TransferCreate) -> dict | None:
    """
    Сохраняет новый документ трансфера в базе данных.

    :param transfer_data: Pydantic-модель с данными для нового трансфера.
    :return: Словарь с данными созданного документа из БД.
    """
    db: AsyncIOMotorDatabase = get_database()
    collection = db[COLLECTION_NAME]

    # Преобразуем Pydantic модель в словарь
    transfer_dict = transfer_data.model_dump()

    # Добавляем поля со значениями по умолчанию
    transfer_dict["status"] = TransferStatus.SCHEDULED.value
    
    # Вставляем документ в коллекцию
    result = await collection.insert_one(transfer_dict)
    
    # Находим и возвращаем только что созданный документ для подтверждения
    created_document = await collection.find_one({"_id": result.inserted_id})
    if created_document and "_id" in created_document:
        created_document["_id"] = str(created_document["_id"])
    return created_document 