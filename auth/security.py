from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

def _is_bcrypt_safe(password: str) -> bool:
    return len(password.encode("utf-8")) <= 72


def validate_password_strength(password: str) -> None:

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


def hash_password(password: str) -> str:

    validate_password_strength(password)

    if not _is_bcrypt_safe(password):
        raise ValueError("Password too long (max 72 bytes for bcrypt)")

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    if not plain_password or not hashed_password:
        return False

    # 🔥 IMPORTANT: safe reject (no exception)
    if not _is_bcrypt_safe(plain_password):
        return False

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
