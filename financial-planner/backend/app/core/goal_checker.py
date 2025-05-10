def check_goal_feasibility(goal, user_profile):
    if goal.target_amount <= user_profile.total_savings + (goal.months_to_achieve * user_profile.monthly_income):
        return True, "Goal is achievable."
    else:
        return False, "Goal is not achievable with current savings and income."