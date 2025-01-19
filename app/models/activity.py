from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"))

    # Определяем отношение many-to-one с родителем
    parent = relationship(
        "Activity",
        remote_side=[id],
        backref="children",
        cascade="all, delete"
    )

    # Связь с организациями
    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities"
    )