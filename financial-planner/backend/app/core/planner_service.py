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
        # Calculate derived fields
        monthly_surplus = user.income - user.expenses - sum(l.installment for l in user.loans)
        ideal_emergency_fund = 6 * (user.expenses + sum(l.installment for l in user.loans))

        # Prepare prompt with strict structure and hallucination control
        prompt = f"""
        You are an intelligent and cautious financial advisor. Given the user’s actual financial data below, write a clear, concise rationale for their asset allocation.

        DO NOT make up numbers, investment amounts, or generic filler advice. Only explain based on the data provided.

        User Profile:

        Age: {user.age}

        Risk Profile: {user.risk_profile}

        Monthly Surplus: ₹{monthly_surplus}

        Emergency Fund: ₹{user.emergency_fund}

        Ideal Emergency Fund: ₹{ideal_emergency_fund}

        Goals: {[(g.name, g.months_to_achieve) for g in user.goals]}

        Recommended Allocation:

        Equity: {allocation['equity']}%

        Bonds: {allocation['bonds']}%

        Commodities: {allocation['commodities']}%

        Instructions:
        Follow this structure exactly. Do NOT add investment amount assumptions or general market statements. Tie every point to the user profile.

        Summary:
        One-line summary of the risk-return balance strategy behind this mix.

        Equity (80%):
        • Use the user’s age, risk profile, and goal time horizon to explain the high equity exposure.
        • Do NOT say “equities have historically performed well”. Be user-specific.
        • Use short, clear sentences. No jargon.

        Bonds (10%):
        • Explain how bonds help balance risk in this specific context.
        • Relate to emergency fund and monthly surplus if relevant.

        Commodities (10%):
        • Tie commodity exposure to diversification for this user's profile.
        • Avoid vague macro claims like “economic uncertainty”.

        Suggestion:
        One friendly and specific suggestion. Examples:

        “Since you have an aggressive profile and short-term goals, review your portfolio quarterly.”

        “Maintain your emergency fund and avoid over-leveraging despite high surplus.”

        Tone: Friendly, human, professional.
        Return: Plain text only. No Markdown or emojis.

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

        # Stream and assemble response
        output_lines = []
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode('utf-8'))
                chunk = data.get("response", "")
                if chunk:
                    output_lines.append(chunk)
            except json.JSONDecodeError:
                continue

        return "".join(output_lines).strip()
