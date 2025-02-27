from loguru import logger
from geopy.distance import geodesic

from typing import List, Type
from .base import BaseCRUD
from sqlalchemy.orm import Session, joinedload
from app.schemas.building import BuildingResponse
from app.models.building import Building


class BuildingCRUD(BaseCRUD[Building]):
    def __init__(self):
        super().__init__(Building)

    def get_buildings_in_radius(self, db: Session, latitude: float, longitude: float, radius: float) -> List[BuildingResponse]:
        logger.info("Получение зданий в радиусе {radius} км от точки ({lat}, {lon})", radius=radius, lat=latitude,
                    lon=longitude)
        buildings = db.query(self.model).options(joinedload(self.model.organizations)).all()

        def is_within_radius(building):
            return geodesic((latitude, longitude), (building.latitude, building.longitude)).km <= radius

        buildings_in_radius = [building for building in buildings if is_within_radius(building)]

        # Преобразуем результаты в BuildingResponse
        def build_response(building):
            org_ids = [org.id for org in building.organizations] if building.organizations else []
            return BuildingResponse(
                id=building.id,
                address=building.address,
                latitude=building.latitude,
                longitude=building.longitude,
                organizations=org_ids,
                organizations_count=len(org_ids)
            )

        return [build_response(building) for building in buildings_in_radius]