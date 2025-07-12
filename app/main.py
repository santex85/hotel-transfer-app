from fastapi import FastAPI

# Создание экземпляра приложения
app = FastAPI(
    title="Hotel Transfer Hub",
    description="API для управления трансферами в отелях.",
    version="1.0.0"
)

# --- Раздел для будущих доработок ---
# Здесь мы позже добавим обработчики событий для подключения к БД
# и подключим основной роутер нашего API.
#
# from .database import connect_to_mongo, close_mongo_connection
# app.add_event_handler("startup", connect_to_mongo)
# app.add_event_handler("shutdown", close_mongo_connection)
#
# from .api import router as api_router
# app.include_router(api_router, prefix="/api/v1")
# --- Конец раздела ---

@app.get("/", tags=["Health Check"])
async def read_root():
    """
    Эндпоинт для проверки работоспособности API.
    """
    return {"status": "ok", "message": "Welcome to Hotel Transfer Hub API"} 