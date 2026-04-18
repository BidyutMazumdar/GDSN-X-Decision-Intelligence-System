# =========================
# 🔐 AUTH DEPENDENCIES (ABSOLUTE FINAL LOCK 🔒)
# =========================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from auth.auth import SECRET_KEY, ALGORITHM
from db.database import get_db
from db import models

# =========================
# 🔐 TOKEN SCHEME
# =========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# =========================
# 🔐 GET CURRENT USER (FIXED 🔥)
# =========================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Extract and validate user from JWT token
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # ✅ DB থেকে user fetch (CRITICAL FIX)
    user = db.query(models.User).filter(models.User.username == username).first()

    if user is None:
        raise credentials_exception

    return user


# =========================
# 🔐 ADMIN CHECK
# =========================
def require_admin(user = Depends(get_current_user)):

    if user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user
