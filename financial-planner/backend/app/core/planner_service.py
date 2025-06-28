import json
import requests
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
        summary['goal_analysis'] = [self._check_goal_feasibility(goal) for goal in user.goals]

        # 4. Asset Allocation
        allocation = self._calculate_asset_allocation(user)
        summary['recommended_allocation'] = allocation

        # 5. LLM Explanation
        try:
            explanation = self._explain_allocation_with_llm(user, allocation)
        except Exception as e:
            explanation = "Explanation not available due to a system error."
            print("LLM error:", e)
        summary['allocation_explanation'] = explanation

        return summary

    def _calculate_asset_allocation(self, user: User) -> dict:
        base = {
            'conservative': {'equity': 30, 'bonds': 60, 'commodities': 10},
            'balanced': {'equity': 50, 'bonds': 40, 'commodities': 10},
            'aggressive': {'equity': 70, 'bonds': 20, 'commodities': 10}
        }

        allocation = base.get(user.risk_profile.lower(), base['balanced']).copy()

        # Age adjustment
        age_limit = max(0, 110 - user.age)
        if allocation['equity'] > age_limit:
            shift = allocation['equity'] - age_limit
            allocation['equity'] -= shift
            allocation['bonds'] += shift

        # Emergency fund adjustment
        required_emergency = 6 * (user.expenses + sum(l.installment for l in user.loans))
        deficit_ratio = max(0, (required_emergency - user.emergency_fund) / required_emergency)
        if deficit_ratio > 0:
            equity_cut = round(deficit_ratio * 20)
            allocation['equity'] = max(10, allocation['equity'] - equity_cut)
            allocation['bonds'] = min(90, allocation['bonds'] + equity_cut)

        # Surplus adjustment
        total_emi = sum(l.installment for l in user.loans)
        surplus = user.income - user.expenses - total_emi
        surplus_ratio = surplus / user.income
        if surplus_ratio < 0.1:
            allocation['equity'] = max(10, allocation['equity'] - 10)
            allocation['bonds'] += 10
        elif surplus_ratio > 0.3:
            allocation['equity'] = min(90, allocation['equity'] + 10)
            allocation['bonds'] = max(0, allocation['bonds'] - 10)

        # Goal horizon analysis
        short_term_goals = [g for g in user.goals if g.months_to_achieve <= 24]
        long_term_goals = [g for g in user.goals if g.months_to_achieve >= 60]
        if len(short_term_goals) > len(long_term_goals):
            allocation['bonds'] = min(90, allocation['bonds'] + 10)
            allocation['equity'] = max(10, allocation['equity'] - 10)

        # Normalize to 100%
        total = sum(allocation.values())
        if total != 100:
            diff = 100 - total
            allocation['commodities'] += diff

        return allocation

    def _check_goal_feasibility(self, goal) -> dict:
        n = goal.months_to_achieve
        P = goal.current_savings
        SIP = goal.sip
        target = goal.target_amount

        # Return rate
        if n <= 36:
            r_annual = 0.06
        elif 36 < n <= 84:
            r_annual = 0.08
        else:
            r_annual = 0.10
        r_monthly = r_annual / 12

        # Future value
        future_value = P * pow(1 + r_monthly, n) + SIP * (((pow(1 + r_monthly, n) - 1) / r_monthly) * (1 + r_monthly))
        feasible = future_value >= target

        result = {
            "name": goal.name,
            "target": round(target, 2),
            "horizon_months": n,
            "expected_return_annual": round(r_annual * 100, 2),
            "projected_value": round(future_value, 2),
            "feasible": feasible
        }

        if not feasible:
            # Suggest higher SIP
            remaining = target - (P * pow(1 + r_monthly, n))
            sip_needed = remaining / (((pow(1 + r_monthly, n) - 1) / r_monthly) * (1 + r_monthly))
            sip_needed = round(sip_needed, 2)

            # Suggest extended time
            extra_months = 0
            fv = future_value
            while fv < target and extra_months < 120:
                extra_months += 1
                total_months = n + extra_months
                fv = P * pow(1 + r_monthly, total_months) + SIP * (
                    ((pow(1 + r_monthly, total_months) - 1) / r_monthly) * (1 + r_monthly))

            result["recommendation"] = {
                "suggested_sip": sip_needed,
                "extend_by_months": extra_months if extra_months > 0 else None
            }

        return result

    def _explain_allocation_with_llm(self, user: User, allocation: dict) -> str:
        prompt = f"""
You are a financial advisor. Based on the user's profile and the following data, explain in simple, friendly terms why the asset allocation is:
Equity: {allocation['equity']}%, Bonds: {allocation['bonds']}%, Commodities: {allocation['commodities']}%.

User Profile:
- Age: {user.age}
- Risk Profile: {user.risk_profile}
- Monthly Surplus: {user.income - user.expenses - sum(l.installment for l in user.loans)}
- Emergency Fund: {user.emergency_fund}
- Ideal Emergency Fund: {6 * (user.expenses + sum(l.installment for l in user.loans))}
- Goals: {[(g.name, g.months_to_achieve) for g in user.goals]}

Structure the explanation as:
1. A summary sentence
2. Bullet points explaining the reasoning
3. A closing suggestion or reassurance

Avoid financial jargon. Be friendly and clear.
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    output += data.get("response", "")
                except Exception as e:
                    print("Error decoding line:", e)

        return output.strip()
