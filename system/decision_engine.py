"""
GDSN-X™ Decision Intelligence System
Core Risk Scoring Engine

Author: Bidyut Mazumdar
Version: v1

Description:
This module calculates a weighted risk score based on:
- Economic Risk (40%)
- Political Risk (35%)
- Social Risk (25%)

Features:
- Input validation
- Risk classification
- Dominant risk factor identification
- Actionable recommendation layer

Outputs:
- Risk Score (0–100)
- Risk Level Classification
- Dominant Risk Insight
- Strategic Recommendation
"""

from typing import Tuple


def validate_inputs(economic: float, political: float, social: float) -> None:
    """
    Validate that all inputs are within 0–100 range.
    """
    for value in (economic, political, social):
        if not (0 <= value <= 100):
            raise ValueError("All inputs must be between 0 and 100.")


def risk_score(economic: float, political: float, social: float) -> Tuple[float, str]:
    """
    Calculate weighted risk score.
    """
    validate_inputs(economic, political, social)

    score = (0.4 * economic) + (0.35 * political) + (0.25 * social)

    if score < 40:
        level = "Low Risk"
    elif score < 70:
        level = "Medium Risk"
    else:
        level = "High Risk"

    return round(score, 2), level


def risk_insight(economic: float, political: float, social: float) -> str:
    """
    Identify dominant risk factor.
    """
    risks = {
        "Economic": economic,
        "Political": political,
        "Social": social
    }

    dominant = max(risks, key=risks.get)
    return f"Dominant Risk Factor: {dominant}"


def risk_recommendation(level: str) -> str:
    """
    Provide decision recommendation based on risk level.
    """
    if level == "High Risk":
        return "Avoid or delay decision. Reassess conditions."
    elif level == "Medium Risk":
        return "Proceed with caution. Use phased or limited approach."
    else:
        return "Safe to proceed under current conditions."


def main() -> None:
    """
    CLI interface for manual testing.
    """
    print("=== GDSN-X™ Decision Intelligence Engine v1.1 ===")

    try:
        economic = float(input("Enter Economic Risk (0-100): "))
        political = float(input("Enter Political Risk (0-100): "))
        social = float(input("Enter Social Risk (0-100): "))

        score, level = risk_score(economic, political, social)
        insight = risk_insight(economic, political, social)
        recommendation = risk_recommendation(level)

        print("\n=== Result ===")
        print(f"Risk Score: {score}")
        print(f"Risk Level: {level}")
        print(insight)
        print(f"Recommendation: {recommendation}")

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
