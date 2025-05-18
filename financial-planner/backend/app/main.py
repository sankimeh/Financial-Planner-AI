from fastapi import FastAPI, HTTPException

from app.core.goal_suggester import GoalSuggester
from app.core.planner_service import PlannerService
from app.core.recommender_engine import query_ollama_for_portfolio
from app.models.user import User

app = FastAPI()
planner = PlannerService()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Financial Planner API is running!"}

@app.post("/analyze")
def analyze_user(user: User):
    return planner.analyze_user(user)

@app.post("/suggest-goals/")
async def suggest_goals(user_data: User):
    suggester = GoalSuggester(user_data)
    suggested_goals = suggester.suggest_goals()
    return {"suggested_goals": suggested_goals}


@app.post("/get_stock_recommendations/")
async def get_stock_recommendations(user: User):
    try:
        # First, analyze the user's financial situation
        summary = planner.analyze_user(user)
        allocation = summary.get('recommended_allocation')
        # Query Ollama for stock recommendations based on user's profile and allocation
        stock_recommendations = query_ollama_for_portfolio(user, allocation)

        return {"summary": summary, "recommendations": stock_recommendations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")