from typing import List, Tuple
from app.models.user import User


class GoalSuggester:
    def __init__(self, user_data: User):
        self.user_data = user_data

    def suggest_goals(self) -> List[Tuple[str, str]]:
        suggested_goals = []
        total_emi = sum(loan.installment for loan in self.user_data.loans)
        goal_names = [goal.name.lower() for goal in self.user_data.goals]
        insurance_lower = [ins.lower() for ins in self.user_data.insurances]
        monthly_surplus = self.user_data.income - self.user_data.expenses - total_emi

        # 1. Emergency Fund
        required_emergency_fund = 6 * (self.user_data.expenses + total_emi)
        if self.user_data.emergency_fund < required_emergency_fund:
            suggested_goals.append((
                "Start/Increase Emergency Fund",
                "You should ideally have 6 months' worth of expenses and EMIs saved to cover unexpected situations."
            ))

        # 2. Life Insurance
        if self.user_data.dependents > 0 and not any("life" in ins for ins in insurance_lower):
            suggested_goals.append((
                "Get Life Insurance",
                "Since you have dependents, life insurance is essential to provide financial protection in case something happens to you."
            ))

        # 3. Health Insurance
        if self.user_data.income > 0 and not any("health" in ins for ins in insurance_lower):
            suggested_goals.append((
                "Get Health Insurance",
                "Medical expenses can be unpredictable and costly. Health insurance helps prevent financial strain during medical emergencies."
            ))

        # 4. Auto Insurance
        if any("car" in loan.type.lower() for loan in self.user_data.loans) and \
           not any("auto" in ins or "car" in ins for ins in insurance_lower):
            suggested_goals.append((
                "Get Auto Insurance",
                "You have a car loan, but no auto insurance found. Insurance protects against vehicle damage, theft, and accidents."
            ))

        # 5. Homeowners/Renters Insurance
        if any("home" in goal.name.lower() for goal in self.user_data.goals) or \
           (self.user_data.expenses > 0.3 * self.user_data.income and not any("home" in ins or "rent" in ins for ins in insurance_lower)):
            suggested_goals.append((
                "Consider Homeowners or Renters Insurance",
                "Property or rental insurance safeguards your living space and belongings against risks like fire, theft, and damage."
            ))

        # 6. Disability Insurance
        if self.user_data.income > 50000 and not any("disability" in ins for ins in insurance_lower):
            suggested_goals.append((
                "Get Disability Insurance",
                "If you're earning well, disability insurance can protect your income in case you're unable to work due to illness or injury."
            ))

        # 7. Long-term Care Insurance
        if self.user_data.age >= 50 and not any("long-term care" in ins for ins in insurance_lower):
            suggested_goals.append((
                "Plan for Long-Term Care Insurance",
                "As you age, the risk of needing long-term medical care increases. Planning ahead can ease the financial burden later."
            ))

        # 8. Travel Insurance
        if any("travel" in goal.name.lower() for goal in self.user_data.goals) and \
           not any("travel" in ins for ins in insurance_lower):
            suggested_goals.append((
                "Consider Travel Insurance",
                "You have travel-related goals, but no travel insurance. It helps cover medical emergencies, cancellations, and losses abroad."
            ))

        # 9. Retirement Planning
        if self.user_data.age >= 30 and 'retirement' not in goal_names:
            suggested_goals.append((
                "Plan for Retirement Savings",
                "Starting retirement planning early allows you to benefit from compounding and build a secure future."
            ))
        elif self.user_data.age >= 50 and 'retirement' in goal_names:
            suggested_goals.append((
                "Accelerate Retirement Planning",
                "As you near retirement, it's time to maximize contributions and align investments with your retirement goals."
            ))

        # 10. High-Interest Debt
        if any(loan.interest_rate > 10 for loan in self.user_data.loans):
            suggested_goals.append((
                "Focus on High-Interest Debt Repayment",
                "Loans with interest rates above 10% can eat into your savings. Prioritizing their repayment reduces long-term financial pressure."
            ))

        # 11. SIP Investment
        if monthly_surplus > 10000 and 'sip' not in goal_names:
            suggested_goals.append((
                "Start Wealth-Building SIP",
                "With a healthy monthly surplus, starting a SIP (Systematic Investment Plan) can help build long-term wealth through disciplined investing."
            ))

        # 12. Redundant Goals
        for goal in self.user_data.goals:
            if goal.current_savings >= goal.target_amount:
                suggested_goals.append((
                    f"Review '{goal.name}' — Already Achieved",
                    "This goal has already been met. You can reallocate resources to other priorities or mark it as complete."
                ))

        return suggested_goals
