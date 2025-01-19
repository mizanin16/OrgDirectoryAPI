from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_db
from app.routers.base_router import BaseRouter
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.crud.organization import OrganizationCRUD

router = APIRouter()

organization_crud = OrganizationCRUD()


@router.get(
    "/organizations/search-by-name",
    response_model=list[OrganizationResponse],
    tags=["organizations"],  # Указываем, что маршрут относится к "organizations"
)
def search_by_name(
        name: str = Query(..., description="Название организации для поиска"),
        db: Session = Depends(get_db),
):
    """Поиск организаций по имени"""
    return organization_crud.search_by_name(db, name)


@router.get(
    "/organizations/activity/{activity_id}",
    response_model=list[OrganizationResponse],
    tags=["organizations"],  # Указываем, что маршрут относится к "organizations"
)
def get_by_activity(activity_id: int, db: Session = Depends(get_db)):
    """Получение организаций по виду деятельности"""
    return organization_crud.get_organizations_by_activity(db, activity_id)


organization_router = BaseRouter(
    model=Organization,
    schema_create=OrganizationCreate,
    schema_update=OrganizationUpdate,
    schema_response=OrganizationResponse,
)

# Включаем CRUD маршруты
router.include_router(organization_router.router, prefix="/organizations", tags=["organizations"])
