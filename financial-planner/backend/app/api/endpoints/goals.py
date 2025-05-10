from fastapi import APIRouter
from typing import List
from app.models.goal import Goal

router = APIRouter()

# Dummy database to store goals
goal_db = {}

@router.post("/goal")
async def create_goal(goal: Goal):
    if goal.name not in goal_db:
        goal_db[goal.name] = goal
    else:
        goal_db[goal.name].current_savings = goal.current_savings  # Update existing goal
    return {"message": f"Goal '{goal.name}' added successfully", "goal": goal}

@router.get("/goals/{user_id}")
async def get_goals(user_id: str):
    user_goals = [goal for goal in goal_db.values() if goal.name.startswith(user_id)]
    if user_goals:
        return user_goals
    return {"message": "No goals found for this user"}
