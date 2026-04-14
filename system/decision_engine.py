"""
GDSN-X™ Decision Intelligence System
Core Risk Engine — v2 PRO (Production Grade)

Author: Bidyut Mazumdar

Upgrades:
✔ Advanced scoring
✔ Volatility index
✔ Confidence modeling
✔ Smart insights (AI-style)
✔ Data robustness
✔ Full compatibility with dashboard
"""

from typing import Tuple
import statistics


# =========================
# 🔹 SAFE VALIDATION
# =========================
def validate_inputs(economic: float, political: float, social: float) -> None:
    for value in (economic, political, social):
        if not (0 <= value <= 100):
            raise ValueError("Inputs must be between 0–100.")


def safe(value):
    try:
        return float(value)
    except Exception:
        return 0.0


# =========================
# 🔹 CORE SCORE
# =========================
def risk_score(economic: float, political: float, social: float) -> Tuple[float, str]:
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


# =========================
# 🔹 INSIGHT ENGINE
# =========================
def risk_insight(economic: float, political: float, social: float) -> str:
    risks = {
        "Economic": economic,
        "Political": political,
        "Social": social
    }

    sorted_risks = sorted(risks.items(), key=lambda x: x[1], reverse=True)

    primary = sorted_risks[0]
    secondary = sorted_risks[1]

    return (
        f"Primary Risk: {primary[0]} ({primary[1]}) | "
        f"Secondary Risk: {secondary[0]} ({secondary[1]})"
    )


# =========================
# 🔹 RISK PROFILE
# =========================
def risk_profile(economic: float, political: float, social: float) -> str:
    if political > 75:
        return "Geopolitical Fragility"
    elif economic > 75:
        return "Macroeconomic Instability"
    elif social > 75:
        return "Societal Disruption Risk"
    else:
        return "Balanced Risk Structure"


# =========================
# 🔹 VOLATILITY INDEX
# =========================
def risk_volatility(economic: float, political: float, social: float) -> float:
    values = [economic, political, social]
    return round(statistics.pstdev(values), 2)


# =========================
# 🔹 DATA CONFIDENCE
# =========================
def data_confidence(economic: float, political: float, social: float) -> str:
    values = [economic, political, social]

    if any(v == 0 for v in values):
        return "Low (Incomplete Data)"
    elif max(values) - min(values) > 50:
        return "Medium (High Variance)"
    else:
        return "High (Consistent Data)"


# =========================
# 🔹 DECISION CONFIDENCE
# =========================
def decision_confidence(score: float) -> str:
    if score > 75:
        return "Low Confidence (High Risk Environment)"
    elif score > 50:
        return "Moderate Confidence"
    else:
        return "High Confidence"


# =========================
# 🔹 SMART AI INSIGHT
# =========================
def smart_insight(score, level, economic, political, social) -> str:

    if level == "High Risk":
        return (
            "Systemic instability detected. Multi-factor risk alignment suggests "
            "high exposure. Strategic delay or defensive positioning recommended."
        )

    elif level == "Medium Risk":
        return (
            "Moderate volatility environment. Selective optimization and phased "
            "execution strategy advised to mitigate downside exposure."
        )

    else:
        return (
            "Stable environment. Risk factors are controlled. Opportunity for "
            "structured growth and capital deployment."
        )


# =========================
# 🔹 RECOMMENDATION ENGINE
# =========================
def risk_recommendation(level: str, economic: float, political: float, social: float) -> str:

    if level == "High Risk":
        if political > 70:
            return "Severe political instability. Avoid entry or delay decision."
        elif economic > 70:
            return "Economic volatility high. Reduce exposure and hedge risk."
        elif social > 70:
            return "Social unrest risk. Monitor behavioral indicators."
        else:
            return "Overall high risk. Re-evaluate full strategy."

    elif level == "Medium Risk":
        return "Controlled execution recommended. Use phased investment strategy."

    else:
        return "Favorable conditions. Proceed with standard execution strategy."
