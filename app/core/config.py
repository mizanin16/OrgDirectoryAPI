from pydantic import ConfigDict  # Импортируйте ConfigDict из pydantic
from pydantic_settings import BaseSettings  # Импортируйте BaseSettings из pydantic_settings

class Settings(BaseSettings):
    DATABASE_URL: str
    API_KEY: str

    # Используйте ConfigDict вместо Config
    model_config = ConfigDict(env_file=".env")

# Создаем экземпляр настроек
settings = Settings()