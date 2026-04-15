# =========================
# AUTH CORE (JWT SYSTEM)
# =========================

from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
from typing import Optional, Dict


# =========================
# ENV CONFIG (IMPORTANT)
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================
# CREATE TOKEN
# =========================
def create_access_token(data: dict) -> str:
    """
    Create JWT access token with expiry
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()  # issued at (pro feature)
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# DECODE TOKEN
# =========================
def decode_token(token: str) -> Optional[Dict]:
    """
    Decode and validate JWT token
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        return None


# =========================
# VERIFY TOKEN
# =========================
def verify_token(token: str) -> bool:
    """
    Check if token is valid
    """

    return decode_token(token) is not None


# =========================
# GET USER FROM TOKEN
# =========================
def get_username_from_token(token: str) -> Optional[str]:
    """
    Extract username from token (sub field)
    """

    payload = decode_token(token)

    if payload:
        return payload.get("sub")

    return None


# =========================
# OPTIONAL: TOKEN DATA HELPER
# =========================
def get_token_data(token: str) -> Optional[Dict]:
    """
    Return full token payload (advanced use)
    """

    return decode_token(token)
