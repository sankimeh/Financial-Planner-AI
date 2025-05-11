from fastapi import FastAPI

from app.core.goal_suggester import GoalSuggester
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

@app.post("/suggest-goals/")
async def suggest_goals(user_data: User):
    # Pass the User object to GoalSuggester (not dict())
    suggester = GoalSuggester(user_data)
    suggested_goals = suggester.suggest_goals()
    return {"suggested_goals": suggested_goals}