from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException
from typing import Type, List, Any, Callable

from app.core.dependencies import get_db
from app.routers.base_router import BaseRouter
from app.models.activity import Activity
from app.routers.organization import organization_router
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
from app.crud.activity import ActivityCRUD

router = APIRouter()

activity_crud = ActivityCRUD()


@router.get("/activities/")
def get_activities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Загружаем активности с предзагрузкой связей
    activities = (
        db.query(Activity)
        .options(
            joinedload(Activity.children),
            joinedload(Activity.organizations)
        )
        .filter(Activity.parent_id.is_(None))  # Получаем только корневые активности
        .offset(skip)
        .limit(limit)
        .all()
    )

    def build_activity_response(act):
        # Преобразуем организации в список ID
        org_ids = [org.id for org in act.organizations] if act.organizations else []

        return ActivityResponse(
            id=act.id,
            name=act.name,
            parent_id=act.parent_id,
            children=[build_activity_response(child) for child in act.children],
            organizations=org_ids,
            organizations_count=len(org_ids)
        )

    return [build_activity_response(activity) for activity in activities]


@router.get("/activities/{item_id}")
def get_activity(item_id: int, db: Session = Depends(get_db)):
    # Загружаем активность с предзагрузкой связей
    activity = (
        db.query(Activity)
        .options(
            joinedload(Activity.children),
            joinedload(Activity.organizations)
        )
        .filter(Activity.id == item_id)
        .first()
    )

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    def build_activity_response(act):
        # Преобразуем организации в список ID
        org_ids = [org.id for org in act.organizations] if act.organizations else []

        return ActivityResponse(
            id=act.id,
            name=act.name,
            parent_id=act.parent_id,
            children=[build_activity_response(child) for child in act.children],
            organizations=org_ids,
            organizations_count=len(org_ids)
        )

    return build_activity_response(activity)


@router.get("/hierarchy", tags=["activities"])
def get_hierarchy(db: Session = Depends(get_db)):
    """Получение иерархии видов деятельности"""
    return activity_crud.get_hierarchy(db)


activity_router = BaseRouter(
    model=Activity,
    schema_create=ActivityCreate,
    schema_update=ActivityUpdate,
    schema_response=ActivityResponse,
)

router.include_router(activity_router.router, prefix="/activities", tags=["activities"])