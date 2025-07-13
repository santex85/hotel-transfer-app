from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from .schemas import TransferCreate, TransferStatus, TransferPublic, TransferUpdate, UserCreate, UserInDB
from . import auth

# Название коллекции в MongoDB
COLLECTION_NAME = "transfers"
USERS_COLLECTION_NAME = "users"

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

async def get_transfer_by_id(db: AsyncIOMotorDatabase, transfer_id: str) -> dict | None:
    """
    Находит один трансфер по его ID.
    """
    collection = db[COLLECTION_NAME]
    
    try:
        document = await collection.find_one({"_id": ObjectId(transfer_id)})
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document
    except Exception:
        return None

async def update_transfer_by_id(db: AsyncIOMotorDatabase, transfer_id: str, data: TransferUpdate) -> dict | None:
    """
    Обновляет данные трансфера по его ID.
    """
    collection = db[COLLECTION_NAME]
    
    # model_dump(exclude_unset=True) выгружает только те поля, что были переданы
    update_data = data.model_dump(exclude_unset=True)
    
    if not update_data:
        return None # Если нечего обновлять, выходим
        
    await collection.update_one(
        {"_id": ObjectId(transfer_id)},
        {"$set": update_data}
    )
    
    updated_document = await collection.find_one({"_id": ObjectId(transfer_id)})
    if updated_document and "_id" in updated_document:
        updated_document["_id"] = str(updated_document["_id"])
    return updated_document

async def delete_transfer_by_id(db: AsyncIOMotorDatabase, transfer_id: str) -> bool:
    """
    Удаляет трансфер по его ID.
    Возвращает True в случае успеха, иначе False.
    """
    collection = db[COLLECTION_NAME]
    
    delete_result = await collection.delete_one({"_id": ObjectId(transfer_id)})
    
    return delete_result.deleted_count > 0

# Функции для работы с пользователями

async def create_user(db: AsyncIOMotorDatabase, user_data: UserCreate) -> UserInDB:
    """
    Создает нового пользователя с хешированным паролем.
    """
    collection = db[USERS_COLLECTION_NAME]
    
    # Проверяем, что пользователь с таким именем не существует
    existing_user = await collection.find_one({"username": user_data.username})
    if existing_user:
        raise ValueError("Пользователь с таким именем уже существует")
    
    # Создаем хеш пароля
    hashed_password = auth.get_password_hash(user_data.password)
    
    # Создаем документ пользователя
    user_dict = {
        "username": user_data.username,
        "hashed_password": hashed_password
    }
    
    # Вставляем документ в коллекцию
    result = await collection.insert_one(user_dict)
    
    # Возвращаем модель пользователя
    return UserInDB(
        _id=str(result.inserted_id),
        username=user_data.username,
        hashed_password=hashed_password
    )

async def get_user_by_username(db: AsyncIOMotorDatabase, username: str) -> dict | None:
    """
    Находит пользователя по имени пользователя.
    """
    collection = db[USERS_COLLECTION_NAME]
    
    user = await collection.find_one({"username": username})
    if user and "_id" in user:
        user["_id"] = str(user["_id"])
    return user 