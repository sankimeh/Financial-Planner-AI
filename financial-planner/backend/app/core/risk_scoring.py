def calculate_risk_profile(user_profile):
    if user_profile.age < 30:
        return "High Risk"
    elif 30 <= user_profile.age < 50:
        return "Medium Risk"
    else:
        return "Low Risk"