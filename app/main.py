from fastapi import FastAPI
from app.routers import organization, activity, building

app = FastAPI()

app.include_router(organization.router)
app.include_router(activity.router)
app.include_router(building.router)
