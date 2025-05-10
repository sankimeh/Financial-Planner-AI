from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class GoalType(str, Enum):
    RETIREMENT = "Retirement"
    EDUCATION = "Education"
    HOUSE = "House"
    EMERGENCY_FUND = "Emergency Fund"
    VACATION = "Vacation"

class Goal(BaseModel):
    name: str
    goal_type: GoalType
    target_amount: float
    current_savings: float
    months_to_achieve: int
    priority_level: int  # Priority of the goal (e.g., 1 for high priority)
    description: Optional[str] = None
