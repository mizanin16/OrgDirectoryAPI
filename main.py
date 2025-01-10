from fastapi import FastAPI
from app.routers.organization import router as organization_router
from app.core.db import Base, engine

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI()

# Подключение роутеров
app.include_router(organization_router)
