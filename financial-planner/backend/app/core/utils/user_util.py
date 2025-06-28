from app.models.user import User


def get_user_profile_summary(user: User) -> dict:
    short_term, mid_term, long_term = [], [], []
    for goal in user.goals:
        if goal.months_to_achieve <= 24:
            short_term.append(goal.name)
        elif goal.months_to_achieve <= 60:
            mid_term.append(goal.name)
        else:
            long_term.append(goal.name)

    return {
        "name": user.name,
        "risk_profile": user.risk_profile,
        "monthly_surplus": user.monthly_surplus,
        "goal_breakdown": {
            "short_term_goals": short_term,
            "mid_term_goals": mid_term,
            "long_term_goals": long_term
        },
        "has_emergency_fund": user.emergency_fund >= (user.expenses * 6),
        "loan_obligations": [loan.type for loan in user.loans]
    }