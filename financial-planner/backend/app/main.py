from fastapi import FastAPI

from app.core.planner_service import PlannerService
from app.models.user import User

app = FastAPI()
planner = PlannerService()
@app.get("/")
def root():
    return {"message": "Financial Planner API is running!"}

@app.post("/analyze")
def analyze_user(user: User):
    return planner.analyze_user(user)