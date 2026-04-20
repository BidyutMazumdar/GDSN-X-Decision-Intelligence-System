from passlib.context import CryptContext

# =========================
# 🔐 PASSWORD HASH CONFIG
# =========================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

# =========================
# 🔐 INTERNAL: BCRYPT SAFE CHECK
# =========================
def _is_bcrypt_safe(password: str) -> bool:
    """
    Ensure password ≤ 72 bytes (bcrypt limit)
    """
    return len(password.encode("utf-8")) <= 72


# =========================
# 🔐 PASSWORD POLICY (STRICT)
# =========================
def validate_password_strength(password: str) -> None:
    """
    Enforce strong password policy
    """

    if not password or not password.strip():
        raise ValueError("Password cannot be empty")

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    if not any(c.isupper() for c in password):
        raise ValueError("Password must include at least one uppercase letter")

    if not any(c.islower() for c in password):
        raise ValueError("Password must include at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        raise ValueError("Password must include at least one digit")


# =========================
# 🔐 HASH PASSWORD (ABSOLUTE FINAL)
# =========================
def hash_password(password: str) -> str:
    """
    Convert plain password → secure hash
    """

    # ✅ Normalize input
    password = password.strip()

    # ✅ Strength validation
    validate_password_strength(password)

    # ✅ Bcrypt safety check (prevents crash)
    if not _is_bcrypt_safe(password):
        raise ValueError("Password too long (max 72 bytes for bcrypt)")

    # ✅ Secure hashing
    return pwd_context.hash(password)


# =========================
# 🔐 VERIFY PASSWORD (SAFE)
# =========================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Safe verification (no crash)
    """

    if not plain_password or not hashed_password:
        return False

    # 🔐 Normalize input
    plain_password = plain_password.strip()

    # 🔥 Safe reject (prevents bcrypt crash)
    if not _is_bcrypt_safe(plain_password):
        return False

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
