from typing import Tuple, Dict
import statistics

# =========================
# VALIDATION
# =========================
def validate_inputs(*values):
    for v in values:
        if not (0 <= v <= 100):
            raise ValueError("All inputs must be between 0–100")

def safe(v):
    try:
        return float(v)
    except:
        return 0.0


# =========================
# DYNAMIC WEIGHTS
# =========================
def get_weights(use_case: str) -> Dict[str, float]:

    if use_case == "Investment Decision":
        return {"E": 0.30, "P": 0.20, "S": 0.15, "T": 0.15, "Env": 0.10, "L": 0.10}

    elif use_case == "Policy Analysis":
        return {"E": 0.15, "P": 0.30, "S": 0.20, "T": 0.10, "Env": 0.15, "L": 0.10}

    elif use_case == "Business Expansion":
        return {"E": 0.35, "P": 0.20, "S": 0.15, "T": 0.10, "Env": 0.10, "L": 0.10}

    # Default (Balanced)
    return {"E": 0.25, "P": 0.20, "S": 0.20, "T": 0.15, "Env": 0.10, "L": 0.10}


# =========================
# STRATEGY MODE
# =========================
def apply_strategy(score: float, strategy: str) -> float:

    if strategy == "Conservative":
        return score + 5
    elif strategy == "Aggressive":
        return score - 5

    return score


# =========================
# CORE RISK MODEL
# =========================
def risk_score(
    economic, political, social,
    tech, env, legal,
    use_case="Balanced",
    strategy="Balanced"
) -> Tuple[float, str, Dict]:

    # Safe cast
    e, p, s = safe(economic), safe(political), safe(social)
    t, en, l = safe(tech), safe(env), safe(legal)

    validate_inputs(e, p, s, t, en, l)

    # Weights
    w = get_weights(use_case)

    # Contributions
    contributions = {
        "Economic": round(w["E"] * e, 2),
        "Political": round(w["P"] * p, 2),
        "Social": round(w["S"] * s, 2),
        "Technological": round(w["T"] * t, 2),
        "Environmental": round(w["Env"] * en, 2),
        "Legal": round(w["L"] * l, 2),
    }

    # Base score
    score = sum(contributions.values())

    # Non-linear penalty
    extreme_flag = any(v > 80 for v in [e, p, s, t, en, l])
    if extreme_flag:
        score += 7

    # Strategy adjustment
    score = apply_strategy(score, strategy)

    # Clamp
    score = max(0, min(score, 100))

    # Risk level
    if score < 40:
        level = "Low Risk"
    elif score < 70:
        level = "Medium Risk"
    else:
        level = "High Risk"

    meta = {
        "weights": w,
        "contributions": contributions,
        "extreme_risk": extreme_flag
    }

    return round(score, 2), level, meta


# =========================
# BACKWARD COMPATIBILITY
# =========================
def risk_score_simple(*args, **kwargs):
    score, level, _ = risk_score(*args, **kwargs)
    return score, level


# =========================
# EXPLAINABILITY (FINAL ELITE)
# =========================
def explain_score(meta):

    # Safe extraction
    contributions = meta.get("contributions", {})

    if not contributions:
        return "No contribution data available for explanation."

    # Zero division safe
    total = sum(contributions.values()) or 1

    # Normalize
    breakdown = {
        k: round((v / total) * 100, 1)
        for k, v in contributions.items()
    }

    # Sort
    sorted_items = sorted(
        breakdown.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Edge cases
    if len(sorted_items) == 1:
        return f"Risk is driven entirely by {sorted_items[0][0]}."

    if len(sorted_items) < 2:
        return "Insufficient data for full explanation."

    # Top drivers
    top, second = sorted_items[0], sorted_items[1]

    # Concentration logic
    concentration = round(top[1] + second[1], 1)

    if concentration > 70:
        intensity = "highly concentrated"
    elif concentration > 50:
        intensity = "moderately concentrated"
    else:
        intensity = "diversified"

    return (
        f"Risk is primarily driven by {top[0]} ({top[1]}%), "
        f"followed by {second[0]} ({second[1]}%). "
        f"Overall risk structure is {intensity}."
    )


# =========================
# INSIGHT
# =========================
def risk_insight(e, p, s, t, en, l):

    data = {
        "Economic": e,
        "Political": p,
        "Social": s,
        "Technological": t,
        "Environmental": en,
        "Legal": l
    }

    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    return f"Primary Driver: {sorted_data[0][0]} | Secondary: {sorted_data[1][0]}"


# =========================
# PROFILE
# =========================
def risk_profile(e, p, s, t, en, l):

    if p > 75:
        return "Geopolitical Fragility"
    if e > 75:
        return "Macroeconomic Instability"
    if t > 75:
        return "Technological Disruption Risk"
    if en > 75:
        return "Environmental Exposure Risk"
    if l > 75:
        return "Regulatory / Legal Uncertainty"

    return "Balanced Multi-Factor Risk"


# =========================
# VOLATILITY
# =========================
def risk_volatility(e, p, s, t, en, l):
    return round(statistics.pstdev([e, p, s, t, en, l]), 2)


# =========================
# DATA CONFIDENCE
# =========================
def data_confidence(e, p, s, t, en, l):

    values = [e, p, s, t, en, l]
    variance = max(values) - min(values)

    score = 100 - variance

    if any(v == 0 for v in values):
        score -= 15

    score = max(0, min(round(score, 2), 100))

    if score > 75:
        label = "High Confidence"
    elif score > 50:
        label = "Moderate Confidence"
    else:
        label = "Low Confidence"

    return {"score": score, "label": label}


# =========================
# DECISION CONFIDENCE
# =========================
def decision_confidence(score):
    return round(100 - abs(score - 50), 2)


# =========================
# SMART INSIGHT
# =========================
def smart_insight(score, level, e, p, s, t, en, l):

    if level == "High Risk":
        return (
            "High systemic risk driven by multi-factor instability. "
            "Structural weaknesses detected. Entry should be delayed or risk-mitigated."
        )

    elif level == "Medium Risk":
        return (
            "Moderate risk with uneven factor distribution. "
            "Opportunities exist with controlled execution."
        )

    return (
        "Low systemic risk with stable macro indicators. "
        "Favorable for expansion and long-term investment."
    )


# =========================
# RECOMMENDATION
# =========================
def risk_recommendation(level, strategy):

    if strategy == "Conservative":
        if level == "High Risk":
            return "Avoid entry or delay decision"
        elif level == "Medium Risk":
            return "Enter cautiously with safeguards"
        return "Proceed with caution"

    elif strategy == "Aggressive":
        if level == "High Risk":
            return "High-risk, high-reward scenario"
        elif level == "Medium Risk":
            return "Capture early advantage"
        return "Expand aggressively"

    # Balanced
    if level == "High Risk":
        return "Reduce exposure and reassess"
    elif level == "Medium Risk":
        return "Phased execution recommended"
    return "Proceed under normal conditions"


# =========================
# DECISION SUMMARY
# =========================
def decision_summary(score, level, confidence):

    return {
        "score": score,
        "risk_level": level,
        "confidence": confidence,
        "decision": (
            "Proceed" if level == "Low Risk"
            else "Caution" if level == "Medium Risk"
            else "Avoid"
        )
    }
