from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.core.db import Base

# Таблица для связи "Организация <-> Деятельность"
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_numbers = Column(ARRAY(String), nullable=False, default=[])
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=True)

    # Связи
    building = relationship(
        "Building",
        back_populates="organizations",
        cascade="all, delete"
    )
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations",
    )
