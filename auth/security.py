# =========================
# 🔐 PASSWORD SECURITY (LOCK 🔒 EDITION)
# GDSN-X™ Enterprise Standard
# =========================

from passlib.context import CryptContext


# =========================
# 🔐 HASHING CONFIGURATION
# =========================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12   # 🔐 security cost factor (12 = strong default)
)


# =========================
# 🔐 HASH PASSWORD
# =========================
def hash_password(password: str) -> str:
    """
    Convert plain password → secure hash
    """
    if not password:
        raise ValueError("Password cannot be empty")

    return pwd_context.hash(password)


# =========================
# 🔐 VERIFY PASSWORD
# =========================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password
    """

    if not plain_password or not hashed_password:
        return False

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


# =========================
# 🔐 OPTIONAL: PASSWORD VALIDATION (ELITE)
# =========================
def validate_password_strength(password: str) -> bool:
    """
    Enforce strong password policy
    """

    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit
