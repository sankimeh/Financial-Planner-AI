from pydantic import BaseModel
from typing import List, Optional

from app.models.goal import Goal


class UserProfile(BaseModel):
    name: str
    age: int
    monthly_income: float
    total_savings: float
    monthly_expenses: float
    loans: Optional[List[str]] = []
    emergency_fund: Optional[float] = None
    insurance: Optional[List[str]] = []
    risk_profile: Optional[str] = None  # This will be determined based on inputs, not manually filled
    goals: Optional[List[Goal]] = []