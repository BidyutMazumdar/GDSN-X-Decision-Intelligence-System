"""
GDSN-X™ Decision Intelligence System
Core Risk Scoring Engine — v1 (Enhanced)

Author: Bidyut Mazumdar

Description:
Advanced weighted risk scoring engine with multi-factor insight,
dynamic recommendation logic, and risk profiling.

Model:
- Economic Risk (40%)
- Political Risk (35%)
- Social Risk (25%)

Outputs:
- Risk Score (0–100)
- Risk Level Classification
- Primary & Secondary Risk Insight
- Risk Profile Tag
- Strategic Recommendation
"""

from typing import Tuple


# =========================
# 🔹 VALIDATION
# =========================
def validate_inputs(economic: float, political: float, social: float) -> None:
    for value in (economic, political, social):
        if not (0 <= value <= 100):
            raise ValueError("All inputs must be between 0 and 100.")


# =========================
# 🔹 CORE SCORE
# =========================
def risk_score(economic: float, political: float, social: float) -> Tuple[float, str]:
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
# 🔹 MULTI-FACTOR INSIGHT
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
    if political > 70:
        return "High Political Exposure"
    elif economic > 70:
        return "Economic Dominant Risk"
    elif social > 70:
        return "Social Instability Risk"
    else:
        return "Balanced Risk Profile"


# =========================
# 🔹 DYNAMIC RECOMMENDATION
# =========================
def risk_recommendation(level: str, economic: float, political: float, social: float) -> str:

    if level == "High Risk":
        if political > 70:
            return "High political instability detected. Delay or avoid entry."
        elif economic > 70:
            return "High economic volatility. Reduce investment exposure."
        elif social > 70:
            return "High social instability. Monitor public sentiment closely."
        else:
            return "Overall high risk. Reassess full strategy."

    elif level == "Medium Risk":
        if political > economic and political > social:
            return "Political risk dominant. Use phased or limited entry strategy."
        elif economic > political and economic > social:
            return "Economic risk dominant. Optimize cost and investment scale."
        else:
            return "Moderate uncertainty. Proceed with controlled execution."

    else:
        return "Low risk environment. Proceed under standard conditions."


# =========================
# 🔹 CLI TEST
# =========================
def main() -> None:
    print("=== GDSN-X™ Decision Intelligence Engine v1 ===")

    try:
        economic = float(input("Enter Economic Risk (0-100): "))
        political = float(input("Enter Political Risk (0-100): "))
        social = float(input("Enter Social Risk (0-100): "))

        score, level = risk_score(economic, political, social)
        insight = risk_insight(economic, political, social)
        profile = risk_profile(economic, political, social)
        recommendation = risk_recommendation(level, economic, political, social)

        print("\n=== Result ===")
        print(f"Risk Score: {score}")
        print(f"Risk Level: {level}")
        print(insight)
        print(f"Risk Profile: {profile}")
        print(f"Recommendation: {recommendation}")

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
