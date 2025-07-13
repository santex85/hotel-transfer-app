from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import FastAPI
from .config import settings

def get_database(app: FastAPI) -> AsyncIOMotorDatabase:
    """
    Возвращает экземпляр базы данных MongoDB.
    
    :param app: Экземпляр FastAPI приложения
    :return: AsyncIOMotorDatabase экземпляр
    """
    if not hasattr(app.state, 'mongo_client') or app.state.mongo_client is None:
        raise RuntimeError("Database client not initialized. Call connect_to_mongo() first.")
    
    return app.state.mongo_client[settings.DATABASE_NAME]

async def connect_to_mongo(app: FastAPI):
    """
    Устанавливает подключение к MongoDB.
    """
    app.state.mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Проверяем подключение
    await app.state.mongo_client.admin.command('ping')
    print("✅ Connected to MongoDB!")

async def close_mongo_connection(app: FastAPI):
    """
    Закрывает подключение к MongoDB.
    """
    if hasattr(app.state, 'mongo_client') and app.state.mongo_client:
        app.state.mongo_client.close()
        print("✅ MongoDB connection closed!") 