from typing import List

from app.models.user import User


class GoalSuggester:
    def __init__(self, user_data: User):
        self.user_data = user_data

    def suggest_goals(self) -> List[str]:
        suggested_goals = []
        total_emi = sum(loan.installment for loan in self.user_data.loans)
        # 1. Emergency Fund Suggestion
        if self.user_data.emergency_fund < 6 * (self.user_data.expenses + total_emi):
            suggested_goals.append("Start/Increase Emergency Fund")

        # 2. Insurance Suggestion (for dependents)
        if self.user_data.dependents > 0 and not self.user_data.insurances:
            suggested_goals.append("Get Life/Term Insurance")

        # 3. Retirement Fund Suggestion
        if self.user_data.age > 30 and 'retirement' not in [goal.name.lower() for goal in self.user_data.goals]:
            suggested_goals.append("Plan for Retirement Savings")

        # 4. Debt Repayment Suggestion
        if any(loan.interest_rate > 10 for loan in self.user_data.loans):
            suggested_goals.append("Focus on High-Interest Debt Repayment")

        # 5. Wealth-Building SIP Suggestion
        if self.user_data.monthly_surplus > 10000 and 'sip' not in [goal.name.lower() for goal in self.user_data.goals]:
            suggested_goals.append("Start Wealth-Building SIP")

        return suggested_goals

