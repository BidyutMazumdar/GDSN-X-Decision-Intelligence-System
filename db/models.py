# =========================
# 🧑‍💼 DATABASE MODELS (ULTIMATE LOCK 🔒)
# GDSN-X™ Enterprise SaaS Schema
# =========================

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from db.database import Base


# =========================
# 👤 USER TABLE
# =========================
class User(Base):
    __tablename__ = "users"

    # =========================
    # 🔑 PRIMARY KEY
    # =========================
    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # 👤 USER INFO
    # =========================
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    # =========================
    # 🔐 ACCOUNT STATUS
    # =========================
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # =========================
    # 🧠 FUTURE SaaS EXTENSION (READY)
    # =========================
    plan = Column(String(50), default="free")   # free / pro / enterprise
    api_key = Column(String(255), nullable=True)  # for paid API access

    # =========================
    # 🕒 TIMESTAMPS
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
