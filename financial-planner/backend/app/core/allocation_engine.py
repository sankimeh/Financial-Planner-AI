# core/allocation_engine.py

from typing import Dict

def get_allocation_split(risk_score: str, years_to_goal: int) -> Dict[str, float]:
    """
    Returns recommended allocation percentages for equity, debt, and gold.

    Args:
        risk_score: One of ["low", "moderate", "high"]
        years_to_goal: Time horizon in years

    Returns:
        A dict with keys: 'equity', 'debt', 'gold' and values as percentages
    """
    if risk_score == "low":
        if years_to_goal <= 2:
            return {"equity": 10, "debt": 80, "gold": 10}
        elif years_to_goal <= 5:
            return {"equity": 30, "debt": 60, "gold": 10}
        else:
            return {"equity": 40, "debt": 50, "gold": 10}

    elif risk_score == "moderate":
        if years_to_goal <= 2:
            return {"equity": 20, "debt": 70, "gold": 10}
        elif years_to_goal <= 5:
            return {"equity": 50, "debt": 40, "gold": 10}
        else:
            return {"equity": 60, "debt": 30, "gold": 10}

    elif risk_score == "high":
        if years_to_goal <= 2:
            return {"equity": 30, "debt": 60, "gold": 10}
        elif years_to_goal <= 5:
            return {"equity": 65, "debt": 25, "gold": 10}
        else:
            return {"equity": 75, "debt": 15, "gold": 10}

    else:
        raise ValueError("Invalid risk score. Must be 'low', 'moderate', or 'high'.")
