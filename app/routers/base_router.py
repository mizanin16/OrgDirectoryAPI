from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Type, List, Any, Callable
from pydantic import BaseModel
from app.core.dependencies import get_db


class BaseRouter:
    def __init__(
        self,
        model: Type[Any],
        schema_create: Type[BaseModel],
        schema_update: Type[BaseModel],
        schema_response: Type[BaseModel],
    ):
        self.model = model
        self.schema_create = schema_create
        self.schema_update = schema_update
        self.schema_response = schema_response
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        # CRUD
        @self.router.get("/", response_model=List[self.schema_response])
        def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
            """Получение списка объектов с пагинацией"""
            query = db.query(self.model).offset(skip).limit(limit)
            return query.all()

        @self.router.get("/{item_id}", response_model=self.schema_response)
        def read_item(item_id: int, db: Session = Depends(get_db)):
            """Получение объекта по ID"""
            item = db.get(self.model, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return item

        @self.router.post("/", response_model=self.schema_response)
        def create_item(item: self.schema_create, db: Session = Depends(get_db)):
            """Создание нового объекта"""
            db_item = self.model(**item.model_dump())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item

        @self.router.put("/{item_id}", response_model=self.schema_response)
        def update_item(item_id: int, item: self.schema_update, db: Session = Depends(get_db)):
            """Обновление объекта"""
            db_item = db.get(self.model, item_id)
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")
            for key, value in item.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            db.commit()
            db.refresh(db_item)
            return db_item

        @self.router.delete("/{item_id}")
        def delete_item(item_id: int, db: Session = Depends(get_db)):
            """Удаление объекта"""
            db_item = db.get(self.model, item_id)
            if not db_item:
                raise HTTPException(status_code=404, detail="Item not found")
            db.delete(db_item)
            db.commit()
            return {"message": "Item deleted successfully"}
