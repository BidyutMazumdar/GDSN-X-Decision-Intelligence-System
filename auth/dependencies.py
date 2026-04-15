# =========================
# 🔐 AUTH DEPENDENCIES (LOCK 🔒 EDITION)
# GDSN-X™ Enterprise Security Layer
# =========================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from auth.auth import SECRET_KEY, ALGORITHM


# =========================
# 🔐 TOKEN SCHEME
# =========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/login")


# =========================
# 🔐 GET CURRENT USER
# =========================
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extract and validate user from JWT token
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token"
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )


# =========================
# 🔐 OPTIONAL: ROLE CHECK (FUTURE READY)
# =========================
def require_admin(user: str = Depends(get_current_user)) -> str:
    """
    Example role-based access (extend later)
    """

    if user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user
