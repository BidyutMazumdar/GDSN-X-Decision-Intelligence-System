# =========================
# 🧑‍💼 DATABASE MODELS (LOCK 🔒 EDITION)
# GDSN-X™ Enterprise Schema
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
    email = Column(String(100), unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    # =========================
    # 🔐 ACCOUNT STATUS
    # =========================
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # =========================
    # 🕒 TIMESTAMPS
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
