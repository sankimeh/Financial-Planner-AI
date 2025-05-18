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
            goal_result = self._check_goal_feasibility(goal)
            goal_results.append(goal_result)
        summary['goal_analysis'] = goal_results

        # 4. Asset Allocation
        allocation = self._calculate_asset_allocation(user)
        summary['recommended_allocation'] = allocation

        return summary

    def _check_goal_feasibility(self, goal):
        n = goal.months_to_achieve
        P = goal.current_savings
        SIP = goal.sip
        target = goal.target_amount

        # 1. Dynamic return rate based on horizon
        if n <= 36:
            r_annual = 0.06
        elif 36 < n <= 84:
            r_annual = 0.08
        else:
            r_annual = 0.10
        r_monthly = r_annual / 12

        # 2. Future Value formula
        future_value = P * pow(1 + r_monthly, n) + SIP * (((pow(1 + r_monthly, n) - 1) / r_monthly) * (1 + r_monthly))

        # 3. Feasibility
        feasible = future_value >= target

        result = {
            "name": goal.name,
            "target": round(target, 2),
            "horizon_months": n,
            "expected_return_annual": round(r_annual * 100, 2),
            "projected_value": round(future_value, 2),
            "feasible": feasible
        }

        # 4. Recommendations if not feasible
        if not feasible:
            # Recommend higher SIP
            remaining = target - (P * pow(1 + r_monthly, n))
            sip_needed = remaining / (((pow(1 + r_monthly, n) - 1) / r_monthly) * (1 + r_monthly))
            sip_needed = round(sip_needed, 2)

            # Recommend extended time for same SIP
            extra_months = 0
            fv = future_value
            while fv < target and extra_months < 120:  # Cap to 10 more years
                extra_months += 1
                total_months = n + extra_months
                fv = P * pow(1 + r_monthly, total_months) + SIP * (
                    ((pow(1 + r_monthly, total_months) - 1) / r_monthly) * (1 + r_monthly))

            result["recommendation"] = {
                "suggested_sip": sip_needed,
                "extend_by_months": extra_months if extra_months > 0 else None
            }

        return result

    def _calculate_asset_allocation(self, user: User):
        base = {
            'conservative': {'equity': 30, 'bonds': 60, 'commodities': 10},
            'balanced': {'equity': 50, 'bonds': 40, 'commodities': 10},
            'aggressive': {'equity': 70, 'bonds': 20, 'commodities': 10}
        }

        allocation = base.get(user.risk_profile.lower(), base['balanced']).copy()

        # 1. Age adjustment
        age_limit = max(0, 110 - user.age)
        if allocation['equity'] > age_limit:
            shift = allocation['equity'] - age_limit
            allocation['equity'] -= shift
            allocation['bonds'] += shift

        # 2. Emergency fund adjustment
        required_emergency = 6 * (user.expenses + sum(l.installment for l in user.loans))
        deficit_ratio = max(0, (required_emergency - user.emergency_fund) / required_emergency)
        if deficit_ratio > 0:
            equity_cut = round(deficit_ratio * 20)  # Max 20% reduction
            allocation['equity'] = max(10, allocation['equity'] - equity_cut)
            allocation['bonds'] = min(90, allocation['bonds'] + equity_cut)

        # 3. Surplus adjustment
        total_emi = sum(l.installment for l in user.loans)
        surplus = user.income - user.expenses - total_emi
        surplus_ratio = surplus / user.income
        if surplus_ratio < 0.1:
            allocation['equity'] = max(10, allocation['equity'] - 10)
            allocation['bonds'] += 10
        elif surplus_ratio > 0.3:
            allocation['equity'] = min(90, allocation['equity'] + 10)
            allocation['bonds'] = max(0, allocation['bonds'] - 10)

        # 4. Goal horizon analysis
        short_term_goals = [g for g in user.goals if g.months_to_achieve <= 24]
        long_term_goals = [g for g in user.goals if g.months_to_achieve >= 60]
        if len(short_term_goals) > len(long_term_goals):
            allocation['bonds'] = min(90, allocation['bonds'] + 10)
            allocation['equity'] = max(10, allocation['equity'] - 10)

        # Normalize to sum 100
        total = sum(allocation.values())
        if total != 100:
            diff = 100 - total
            allocation['commodities'] += diff

        return allocation
