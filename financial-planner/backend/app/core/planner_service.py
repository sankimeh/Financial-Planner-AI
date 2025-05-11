
from math import pow

from app.models.user import User


class PlannerService:

    def analyze_user(self, user: User) -> dict:
        summary = {}

        # 1. Monthly surplus
        total_emi = sum(loan.installment for loan in user.loans)
        surplus = user.income - user.expenses - total_emi
        summary['monthly_surplus'] = surplus

        # 2. Emergency fund check
        ideal_emergency = 6 * (user.expenses + total_emi)
        emergency_ok = user.emergency_fund >= ideal_emergency
        summary['emergency_fund_ok'] = emergency_ok
        summary['ideal_emergency_fund'] = ideal_emergency

        # 3. Goal feasibility
        goal_results = []
        for goal in user.goals:
            goal_ok, fv = self._check_goal_feasibility(goal)
            goal_results.append({
                "name": goal.name,
                "target": goal.target_amount,
                "fv": round(fv, 2),
                "feasible": goal_ok
            })
        summary['goal_analysis'] = goal_results

        # 4. Asset Allocation
        allocation = self._calculate_asset_allocation(user)
        summary['recommended_allocation'] = allocation

        return summary

    def _check_goal_feasibility(self, goal):
        r = 0.10 / 12  # Assuming 10% annual return
        n = goal.months_to_achieve
        P = goal.current_savings
        SIP = goal.sip

        future_value = P * pow(1 + r, n) + SIP * (((pow(1 + r, n) - 1) / r) * (1 + r))
        return future_value >= goal.target_amount, future_value

    def _calculate_asset_allocation(self, user: User):
        base_allocations = {
            'conservative': {'equity': 30, 'bonds': 60, 'commodities': 10},
            'balanced': {'equity': 50, 'bonds': 40, 'commodities': 10},
            'aggressive': {'equity': 70, 'bonds': 20, 'commodities': 10}
        }

        allocation = base_allocations.get(user.risk_profile.lower(), base_allocations['balanced'])

        # Adjust for emergency fund
        if user.emergency_fund < (6 * (user.expenses + sum(l.installment for l in user.loans))):
            allocation['equity'] = max(20, allocation['equity'] - 10)
            allocation['bonds'] += 10

        # Adjust for age (simplified age rule)
        age_based_equity = max(0, 110 - user.age)
        if allocation['equity'] > age_based_equity:
            shift = allocation['equity'] - age_based_equity
            allocation['equity'] = age_based_equity
            allocation['bonds'] += shift

        return allocation
