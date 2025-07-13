from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import connect_to_mongo, close_mongo_connection
from .api import router as api_router, auth_router

# Создание экземпляра приложения
app = FastAPI(
    title="Hotel Transfer Hub",
    description="API для управления трансферами в отелях.",
    version="1.0.0"
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Разрешаем фронтенд
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Добавляем обработчики событий для управления подключением к БД
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo(app)

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection(app)

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/v1")
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Эндпоинт для проверки работоспособности API.
    """
    return {"status": "ok", "message": "Welcome to Hotel Transfer Hub API"} 