# =========================
# 🧑‍💼 DATABASE CONNECTION (LOCK 🔒 EDITION)
# GDSN-X™ Enterprise DB Layer
# =========================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import os


# =========================
# 🔐 DATABASE CONFIG
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set in environment variables")


# =========================
# 🧠 ENGINE (OPTIMIZED)
# =========================
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # connection pool
    max_overflow=20,       # extra connections
    pool_pre_ping=True,    # avoid stale connections
    echo=False             # set True for debug
)


# =========================
# 🧑‍💼 SESSION FACTORY
# =========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================
# 🧱 BASE MODEL
# =========================
Base = declarative_base()


# =========================
# 🔄 DB DEPENDENCY (SAFE)
# =========================
def get_db():
    """
    FastAPI dependency for DB session
    """

    db = SessionLocal()

    try:
        yield db

    except SQLAlchemyError:
        db.rollback()
        raise

    finally:
        db.close()
