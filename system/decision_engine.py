from typing import Tuple
import statistics

# ================= VALIDATION =================
def validate_inputs(economic, political, social):
    for v in (economic, political, social):
        if not (0 <= v <= 100):
            raise ValueError("Inputs must be 0–100")


def safe(v):
    try:
        return float(v)
    except:
        return 0.0


# ================= CORE SCORE =================
def risk_score(economic, political, social) -> Tuple[float, str]:

    economic, political, social = safe(economic), safe(political), safe(social)

    validate_inputs(economic, political, social)

    score = (0.4 * economic) + (0.35 * political) + (0.25 * social)

    if score < 40:
        level = "Low Risk"
    elif score < 70:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return round(score, 2), level


# ================= INSIGHT =================
def risk_insight(economic, political, social):

    data = {
        "Economic": economic,
        "Political": political,
        "Social": social
    }

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    return f"Primary: {sorted_data[0][0]} | Secondary: {sorted_data[1][0]}"


# ================= PROFILE =================
def risk_profile(economic, political, social):

    if political > 75:
        return "Geopolitical Fragility"
    elif economic > 75:
        return "Economic Instability"
    elif social > 75:
        return "Social Disruption"
    return "Balanced"


# ================= VOLATILITY =================
def risk_volatility(economic, political, social):

    values = [economic, political, social]
    return round(statistics.pstdev(values), 2)


# ================= CONFIDENCE =================
def data_confidence(economic, political, social):

    values = [economic, political, social]

    if any(v == 0 for v in values):
        return "Low"
    elif max(values) - min(values) > 50:
        return "Medium"
    return "High"


def decision_confidence(score):

    if score > 75:
        return "Low Confidence"
    elif score > 50:
        return "Medium Confidence"
    return "High Confidence"


# ================= AI INSIGHT =================
def smart_insight(score, level, e, p, s):

    if level == "High Risk":
        return "High systemic risk detected. Defensive strategy required."

    if level == "Medium Risk":
        return "Moderate risk environment. Controlled execution advised."

    return "Stable environment. Growth opportunity detected."


# ================= RECOMMENDATION =================
def risk_recommendation(level, e, p, s):

    if level == "High Risk":
        return "Avoid or reduce exposure"

    if level == "Medium Risk":
        return "Phased execution recommended"

    return "Proceed normally"
