from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"))

    # Самоссылающиеся связи
    children = relationship(
        "Activity",
        back_populates="parent",
        remote_side=[id],
        cascade="all, delete"
    )
    parent = relationship(
        "Activity",
        back_populates="children",
        uselist=False
    )

    # Связь с организациями
    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities"
    )
