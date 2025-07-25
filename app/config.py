import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения.
    Считывает переменные из .env файла.
    """
    # Настройки для подключения к MongoDB
    MONGODB_URL: str
    DATABASE_NAME: str

    # Настройки для JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"  # Фиксированный ключ для разработки
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Загрузка переменных из .env файла
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


# Создаем экземпляр настроек, который будет использоваться в приложении
settings = Settings() 