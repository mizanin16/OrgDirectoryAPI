from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


def get_activity(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()


def get_all_activities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Activity).offset(skip).limit(limit).all()


def create_activity(db: Session, activity_data: ActivityCreate):
    activity = Activity(**activity_data.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def update_activity(db: Session, activity_id: int, activity_data: ActivityUpdate):
    activity = get_activity(db, activity_id)
    if not activity:
        return None
    for key, value in activity_data.dict(exclude_unset=True).items():
        setattr(activity, key, value)
    db.commit()
    db.refresh(activity)
    return activity


def delete_activity(db: Session, activity_id: int):
    activity = get_activity(db, activity_id)
    if activity:
        db.delete(activity)
        db.commit()
    return activity
