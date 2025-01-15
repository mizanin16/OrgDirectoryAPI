from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://test:test@localhost:5432/organization_db"
    TEST_DATABASE_URL: str = "postgresql://test:test@localhost:5432/test_organization_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Делаем нечувствительным к регистру
        extra="ignore"  # Игнорируем лишние переменные окружения
    )

# Создаем кэшированный экземпляр настроек
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()