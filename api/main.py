from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

# ================= ENGINE IMPORT =================
from system.decision_engine import (
    risk_score,
    risk_insight,
    risk_recommendation,
    risk_profile,
    smart_insight,
    data_confidence,
    risk_volatility,
    decision_confidence,
    explain_score
)

from system.simulation import run_simulation


# =========================
# APP INIT
# =========================
app = FastAPI(
    title="GDSN-X™ Decision Intelligence API",
    version="2.5 ELITE",
    description="Probabilistic + Explainable + Simulation-based Risk Intelligence Engine"
)


# =========================
# REQUEST MODEL (STRICT VALIDATION)
# =========================
class RiskInput(BaseModel):
    economic: float = Field(..., ge=0, le=100)
    political: float = Field(..., ge=0, le=100)
    social: float = Field(..., ge=0, le=100)
    tech: float = Field(..., ge=0, le=100)
    env: float = Field(..., ge=0, le=100)
    legal: float = Field(..., ge=0, le=100)

    use_case: str
    strategy: str

    iterations: int = Field(default=1000, ge=100, le=10000)


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "GDSN-X API Running 🚀",
        "version": "2.5 ELITE"
    }


# =========================
# CORE ENDPOINT
# =========================
@app.post("/api/v2/risk")
def calculate(data: RiskInput) -> Dict:

    try:
        # ================= CORE MODEL =================
        score, level, meta = risk_score(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal,
            data.use_case,
            data.strategy
        )

        # ================= EXPLAINABILITY =================
        explanation = explain_score(meta)

        insight = risk_insight(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal
        )

        analysis = smart_insight(
            score, level,
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal
        )

        # ================= RISK STRUCTURE =================
        profile = risk_profile(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal
        )

        volatility = risk_volatility(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal
        )

        # ================= CONFIDENCE =================
        confidence = data_confidence(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal
        )

        decision_conf = decision_confidence(score)

        # ================= RECOMMENDATION =================
        recommendation = risk_recommendation(level, data.strategy)

        # ================= MONTE CARLO SIMULATION =================
        simulation = run_simulation(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal,
            data.use_case,
            data.strategy,
            iterations=data.iterations
        )

        # ================= FINAL RESPONSE =================
        return {
            "core": {
                "score": score,
                "risk_level": level,
                "decision_confidence": decision_conf
            },
            "explainability": {
                "explanation": explanation,
                "insight": insight,
                "analysis": analysis
            },
            "risk_structure": {
                "profile": profile,
                "volatility": volatility
            },
            "confidence": {
                "label": confidence["label"],
                "score": confidence["score"]
            },
            "recommendation": recommendation,
            "simulation": {
                "mean": simulation["mean"],
                "min": simulation["min"],
                "max": simulation["max"],
                "std_dev": simulation["std_dev"],
                "high_risk_probability": simulation["high_risk_probability"]
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Error: {str(e)}"
        )
