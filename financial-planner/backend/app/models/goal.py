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
    target_amount: float
    months_to_achieve: int
    current_savings: float
    sip: float  # Monthly SIP
    priority: int  # 1 = highest
