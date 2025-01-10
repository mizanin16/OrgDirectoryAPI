from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
from app.crud.activity import (
    get_activity,
    get_all_activities,
    create_activity,
    update_activity,
    delete_activity,
)

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=list[ActivityResponse])
def get_activities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_activities(db, skip, limit)


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity_by_id(activity_id: int, db: Session = Depends(get_db)):
    activity = get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/", response_model=ActivityResponse)
def create_new_activity(activity_data: ActivityCreate, db: Session = Depends(get_db)):
    return create_activity(db, activity_data)


@router.put("/{activity_id}", response_model=ActivityResponse)
def update_existing_activity(
    activity_id: int, activity_data: ActivityUpdate, db: Session = Depends(get_db)
):
    activity = update_activity(db, activity_id, activity_data)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.delete("/{activity_id}")
def delete_existing_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = delete_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"detail": "Activity deleted successfully"}
