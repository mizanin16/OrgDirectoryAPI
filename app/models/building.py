from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.db import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Связь
    organizations = relationship(
        "Organization",
        back_populates="building",
        cascade="all, delete"
    )
