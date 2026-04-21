# =========================
# 🔐 GDSN-X™ ENTERPRISE API (ULTIMATE LOCK EDITION)
# =========================

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from sqlalchemy.orm import Session
import logging

# =========================
# 🔐 LOGGING CONFIG
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
from db import models, crud

# =========================
# AUTH LAYER
# =========================
from auth.dependencies import get_current_user
from auth.auth import create_access_token

# =========================
# APP INIT
# =========================
app = FastAPI(
    title="GDSN-X™ Enterprise Decision API",
    version="4.0 ULTIMATE",
    description="Enterprise-grade AI Decision Intelligence Engine"
)

# =========================
# STARTUP EVENT
# =========================
@app.on_event("startup")
def on_startup():
    logger.info("🚀 GDSN-X API started (Ultimate Lock Edition)")

# =========================
# GLOBAL ERROR HANDLER
# =========================
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):

    if isinstance(exc, FastAPIHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    logger.exception("Unhandled error")

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# =========================
# REQUEST MODELS
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


class LoginInput(BaseModel):
    username: str
    password: str


class RegisterInput(BaseModel):
    username: str
    email: str
    password: str

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "GDSN-X Enterprise API Running",
        "version": "4.0 ULTIMATE"
    }

# =========================
# LOGIN API
# =========================
@app.post("/login")
def login(data: LoginInput, db: Session = Depends(get_db)):

    try:
        user = crud.verify_user(db, data.username, data.password)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "sub": user.username,
            "user_id": user.id
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Login error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# =========================
# REGISTER API
# =========================
@app.post("/register")
def register(data: RegisterInput, db: Session = Depends(get_db)):

    try:
        user = crud.create_user(
            db,
            data.username,
            data.email,
            data.password
        )

        if not user:
            raise HTTPException(status_code=400, detail="User already exists")

        return {"message": "User created successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except HTTPException:
        raise

    except Exception:
        logger.exception("Register error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# =========================
# RISK ENGINE
# =========================
@app.post("/api/v3/risk")
def calculate_risk(
    data: RiskInput,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> Dict:

    try:
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

        confidence = data_confidence(
            data.economic,
            data.political,
            data.social,
            data.tech,
            data.env,
            data.legal
        )

        decision_conf = decision_confidence(score)
        recommendation = risk_recommendation(level, data.strategy_mode)

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

    except Exception:
        logger.exception("Risk engine error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# =========================
# HISTORY
# =========================
@app.get("/api/v3/history")
def get_history(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    try:
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

    except Exception:
        logger.exception("History fetch error")
        raise HTTPException(status_code=500, detail="Internal Server Error")
