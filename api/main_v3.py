# =========================
# 🏢 GDSN-X™ ENTERPRISE API (FINAL v3)
# =========================

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Optional
from sqlalchemy.orm import Session

# =========================
# ENGINE IMPORT
# =========================
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
# DB LAYER
# =========================
from db.database import get_db
from db import models

# =========================
# AUTH LAYER
# =========================
from auth.dependencies import get_current_user


# =========================
# APP INIT
# =========================
app = FastAPI(
    title="GDSN-X™ Enterprise Decision API",
    version="3.0 ENTERPRISE",
    description="Multi-user SaaS AI Decision Intelligence Engine"
)


# =========================
# REQUEST MODEL
# =========================
class RiskInput(BaseModel):
    economic: float = Field(..., ge=0, le=100)
    political: float = Field(..., ge=0, le=100)
    social: float = Field(..., ge=0, le=100)
    tech: float = Field(..., ge=0, le=100)
    env: float = Field(..., ge=0, le=100)
    legal: float = Field(..., ge=0, le=100)

    use_case: str
    strategy_mode: str

    country: Optional[str] = "N/A"
    iterations: int = Field(default=1000, ge=100, le=10000)


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "GDSN-X Enterprise API Running 🚀",
        "version": "3.0 ENTERPRISE"
    }


# =========================
# 🚀 RISK ENGINE (CORE)
# =========================
@app.post("/api/v3/risk")
def calculate_risk(
    data: RiskInput,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict:

    try:
        # ================= CORE ENGINE =================
        score, level, meta = risk_score(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal,
            data.use_case,
            data.strategy_mode
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
            score,
            level,
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal
        )

        # ================= STRUCTURE =================
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
        recommendation = risk_recommendation(level, data.strategy_mode)

        # ================= SIMULATION =================
        simulation = run_simulation(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal,
            data.use_case,
            data.strategy_mode,
            iterations=data.iterations
        )

        # ================= DB SAVE =================
        record = models.Analysis(
            user_id=user.id,
            country=data.country,
            score=score,
            level=level,
            payload=data.dict(),
            result={
                "analysis": analysis,
                "recommendation": recommendation,
                "decision_conf": decision_conf
            }
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        # ================= RESPONSE =================
        return {
            "core": {
                "score": score,
                "level": level,
                "decision_conf": decision_conf
            },
            "explainability": {
                "explanation": explanation,
                "insight": insight,
                "analysis": analysis
            },
            "structure": {
                "profile": profile,
                "volatility": volatility
            },
            "confidence": {
                "label": confidence["label"],
                "score": confidence["score"]
            },
            "recommendation": recommendation,
            "simulation": simulation,
            "meta": {
                "analysis_id": record.id,
                "user_id": user.id
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Engine Error: {str(e)}"
        )


# =========================
# 📊 HISTORY (SAAS CORE)
# =========================
@app.get("/api/v3/history")
def get_history(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    records = db.query(models.Analysis)\
        .filter(models.Analysis.user_id == user.id)\
        .order_by(models.Analysis.created_at.desc())\
        .all()

    return [
        {
            "id": r.id,
            "country": r.country,
            "score": r.score,
            "level": r.level,
            "created_at": r.created_at
        }
        for r in records
    ]
