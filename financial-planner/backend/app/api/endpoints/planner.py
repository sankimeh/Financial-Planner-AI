from fastapi import APIRouter
from typing import List
from random import randint
from app.models.plan import FinancialPlan

router = APIRouter()

# Dummy function to simulate asset allocation
def generate_asset_allocation() -> dict:
    return {
        "stocks_percentage": randint(40, 60),
        "bonds_percentage": randint(20, 40),
        "gold_percentage": 100 - (randint(40, 60) + randint(20, 40))
    }

@router.post("/plan")
async def create_plan(user_id: str, goal_ids: List[str]):
    # Placeholder logic to create a plan
    recommendations = []  # To store asset recommendations
    for goal_id in goal_ids:
        recommendations.append({
            "asset_class": "stocks",
            "name": f"Recommendation for {goal_id}",
            "ticker": f"STK{randint(1000, 9999)}",
            "risk_level": "Moderate",
            "expected_return": randint(5, 15),
            "rationale": "Based on market trends"
        })

    plan = FinancialPlan(
        user_id=user_id,
        total_amount_needed=1000000,  # Placeholder total goal amount
        asset_allocation=generate_asset_allocation(),
        investment_recommendations=recommendations,
        goal_analysis="Goals are achievable with current savings and investment strategy.",
        risk_profile="Moderate",
        missing_goals=["Emergency Fund"]  # Placeholder
    )

    return plan
