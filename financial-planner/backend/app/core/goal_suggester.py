from typing import List

from app.models.user import User


class GoalSuggester:
    def __init__(self, user_data: User):
        self.user_data = user_data

    def suggest_goals(self) -> List[str]:
        suggested_goals = []

        # 1. Emergency Fund Suggestion
        if self.user_data.emergency_fund < 6 * self.user_data.expenses:
            suggested_goals.append("Start an Emergency Fund")

        # 2. Insurance Suggestion (for dependents)
        if self.user_data.dependents > 0 and not self.user_data.insurances:
            suggested_goals.append("Get Life/Term Insurance")

        # 3. Retirement Fund Suggestion
        if self.user_data.age > 30 and 'retirement' not in [goal.name.lower() for goal in self.user_data.goals]:
            suggested_goals.append("Plan for Retirement Savings")

        # 4. Education Fund Suggestion (for children under 15)
        if self.user_data.dependents > 0:
            children = self.user_data.children or []  # Use empty list if children is None
            for child in children:
                if child['age'] < 15 and 'education' not in [goal.name.lower() for goal in self.user_data.goals]:
                    suggested_goals.append(f"Set up Education Fund for {child['name']}")

        # 5. Debt Repayment Suggestion
        if any(loan.interest_rate > 10 for loan in self.user_data.loans):
            suggested_goals.append("Focus on High-Interest Debt Repayment")

        # 6. Wealth-Building SIP Suggestion
        if self.user_data.monthly_surplus > 10000 and 'sip' not in [goal.name.lower() for goal in self.user_data.goals]:
            suggested_goals.append("Start Wealth-Building SIP")

        return suggested_goals

