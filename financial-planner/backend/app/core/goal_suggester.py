from typing import List
from app.models.user import User


class GoalSuggester:
    def __init__(self, user_data: User):
        self.user_data = user_data

    def suggest_goals(self) -> List[str]:
        suggested_goals = []
        total_emi = sum(loan.installment for loan in self.user_data.loans)
        goal_names = [goal.name.lower() for goal in self.user_data.goals]
        insurance_lower = [ins.lower() for ins in self.user_data.insurances]
        monthly_surplus = self.user_data.income - self.user_data.expenses - total_emi

        # 1. Emergency Fund
        required_emergency_fund = 6 * (self.user_data.expenses + total_emi)
        if self.user_data.emergency_fund < required_emergency_fund:
            suggested_goals.append("Start/Increase Emergency Fund")

        # 2. Life Insurance
        if self.user_data.dependents > 0 and not any("life" in ins for ins in insurance_lower):
            suggested_goals.append("Get Life Insurance")

        # 3. Health Insurance
        if self.user_data.income > 0 and not any("health" in ins for ins in insurance_lower):
            suggested_goals.append("Get Health Insurance")

        # 4. Auto Insurance
        if any("car" in loan.type.lower() for loan in self.user_data.loans) and \
           not any("auto" in ins or "car" in ins for ins in insurance_lower):
            suggested_goals.append("Get Auto Insurance")

        # 5. Homeowners/Renters Insurance
        if any("home" in goal.name.lower() for goal in self.user_data.goals) or \
           (self.user_data.expenses > 0.3 * self.user_data.income and not any("home" in ins or "rent" in ins for ins in insurance_lower)):
            suggested_goals.append("Consider Homeowners or Renters Insurance")

        # 6. Disability Insurance
        if self.user_data.income > 50000 and not any("disability" in ins for ins in insurance_lower):
            suggested_goals.append("Get Disability Insurance")

        # 7. Long-term Care Insurance
        if self.user_data.age >= 50 and not any("long-term care" in ins for ins in insurance_lower):
            suggested_goals.append("Plan for Long-Term Care Insurance")

        # 8. Travel Insurance
        if any("travel" in goal.name.lower() for goal in self.user_data.goals) and \
           not any("travel" in ins for ins in insurance_lower):
            suggested_goals.append("Consider Travel Insurance")

        # 9. Retirement Planning
        if self.user_data.age >= 30 and 'retirement' not in goal_names:
            suggested_goals.append("Plan for Retirement Savings")
        elif self.user_data.age >= 50 and 'retirement' in goal_names:
            suggested_goals.append("Accelerate Retirement Planning")

        # 10. High-Interest Debt
        if any(loan.interest_rate > 10 for loan in self.user_data.loans):
            suggested_goals.append("Focus on High-Interest Debt Repayment")

        # 11. SIP Investment
        if monthly_surplus > 10000 and 'sip' not in goal_names:
            suggested_goals.append("Start Wealth-Building SIP")

        # 12. Redundant Goals
        for goal in self.user_data.goals:
            if goal.current_savings >= goal.target_amount:
                suggested_goals.append(f"Review '{goal.name}' — Already Achieved")

        return suggested_goals
