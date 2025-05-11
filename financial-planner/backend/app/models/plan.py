from pydantic import BaseModel
from typing import List, Optional


class AssetAllocation(BaseModel):
    stocks_percentage: float
    bonds_percentage: float
    gold_percentage: float


class InvestmentRecommendation(BaseModel):
    asset_class: str
    name: str
    ticker: str
    risk_level: str
    expected_return: float
    rationale: str  # Reason behind the recommendation


class FinancialPlan(BaseModel):
    user_id: str
    total_amount_needed: float
    asset_allocation: AssetAllocation
    investment_recommendations: List[InvestmentRecommendation]
    goal_analysis: str  # Analysis if goals are achievable
    action_plan: Optional[str] = None  # Actions to be taken if goals are not achievable
    sentiment_analysis: Optional[str] = None  # Sentiment insights for short-term investments
    risk_profile: str  # Risk profile summary
    missing_goals: Optional[List[str]] = []  # Any missing financial goals like emergency fund
