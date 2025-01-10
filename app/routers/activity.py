from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
from app.crud.activity import (
    get_activity_crud,
    get_all_activities_crud,
    create_activity_crud,
    update_activity_crud,
    delete_activity_crud,
)

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=list[ActivityResponse])
def get_activities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    activities = get_all_activities_crud(db, skip, limit)
    for activity in activities:
        activity.organizations_count = len(activity.organizations)  # Подсчет
    return activities


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity_by_id(activity_id: int, db: Session = Depends(get_db)):
    activity = get_activity_crud(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/", response_model=ActivityResponse)
def create_new_activity(activity_data: ActivityCreate, db: Session = Depends(get_db)):
    return create_activity_crud(db, activity_data)


@router.put("/{activity_id}", response_model=ActivityResponse)
def update_existing_activity(
        activity_id: int, activity_data: ActivityUpdate, db: Session = Depends(get_db)
):
    activity = update_activity_crud(db, activity_id, activity_data)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.delete("/{activity_id}")
def delete_existing_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = delete_activity_crud(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"detail": "Activity deleted successfully"}
