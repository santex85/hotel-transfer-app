from fastapi import FastAPI
from .database import connect_to_mongo, close_mongo_connection
from .api import router as api_router, auth_router

# Создание экземпляра приложения
app = FastAPI(
    title="Hotel Transfer Hub",
    description="API для управления трансферами в отелях.",
    version="1.0.0"
)

# Добавляем обработчики событий для управления подключением к БД
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo(app)

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection(app)

# Подключаем роутеры
app.include_router(auth_router)  # Роутер для аутентификации
app.include_router(api_router, prefix="/api/v1")  # Роутер для трансферов

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Эндпоинт для проверки работоспособности API.
    """
    return {"status": "ok", "message": "Welcome to Hotel Transfer Hub API"} 