# =========================
# 🔐 AUTH DEPENDENCIES (FINAL LOCK 🔒)
# GDSN-X™ Enterprise Security Layer
# =========================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from auth.auth import SECRET_KEY, ALGORITHM


# =========================
# 🔐 TOKEN SCHEME 
# =========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# =========================
# 🔐 GET CURRENT USER
# =========================
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extract and validate user from JWT token
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        return username

    except JWTError:
        raise credentials_exception


# =========================
# 🔐 OPTIONAL: ROLE-BASED ACCESS (FUTURE READY)
# =========================
def require_admin(user: str = Depends(get_current_user)) -> str:
    """
    Example admin-only access control
    """

    if user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user
