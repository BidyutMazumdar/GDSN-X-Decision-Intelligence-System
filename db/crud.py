# =========================
# 🧑‍💼 CRUD OPERATIONS (FINAL LOCK 🔒)
# =========================

from sqlalchemy.orm import Session
from sqlalchemy import or_

from db import models
from auth.security import hash_password, verify_password


# =========================
# CREATE USER
# =========================
def create_user(db: Session, username: str, email: str, password: str):

    # 🔐 Check if user already exists
    existing_user = db.query(models.User).filter(
        or_(
            models.User.username == username,
            models.User.email == email
        )
    ).first()

    if existing_user:
        return None  # 🚨 duplicate user

    # 🔐 Hash password
    hashed_password = hash_password(password)

    # 🧑‍💼 Create user object
    new_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    # 💾 Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# GET USER BY USERNAME
# =========================
def get_user(db: Session, username: str):

    return db.query(models.User).filter(
        models.User.username == username
    ).first()


# =========================
# GET USER BY EMAIL (PRO FEATURE)
# =========================
def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(
        models.User.email == email
    ).first()


# =========================
# VERIFY USER LOGIN
# =========================
def verify_user(db: Session, username: str, password: str):

    user = get_user(db, username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


# =========================
# DELETE USER (ADMIN FEATURE)
# =========================
def delete_user(db: Session, user_id: int):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True
