from pydantic import BaseModel
from typing import List

from app.models.goal import Goal
from app.models.loan import Loan


class User(BaseModel):
    name: str
    age: int
    income: float
    expenses: float
    dependents: int
    emergency_fund: float
    insurances: List[str]
    loans: List[Loan]
    goals: List[Goal]
    risk_profile: str  # 'conservative', 'balanced', 'aggressive'

    @property
    def monthly_surplus(self) -> float:
        return self.income - self.expenses