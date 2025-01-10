from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


def get_activity_crud(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()


def get_all_activities_crud(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Activity).offset(skip).limit(limit).all()


def create_activity_crud(db: Session, activity_data: ActivityCreate):
    activity = Activity(**activity_data.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def update_activity_crud(db: Session, activity_id: int, activity_data: ActivityUpdate):
    activity = get_activity_crud(db, activity_id)
    if not activity:
        return None
    for key, value in activity_data.model_dump(exclude_unset=True).items():
        setattr(activity, key, value)
    db.commit()
    db.refresh(activity)
    return activity


def delete_activity_crud(db: Session, activity_id: int):
    activity = get_activity_crud(db, activity_id)
    if activity:
        db.delete(activity)
        db.commit()
    return activity
