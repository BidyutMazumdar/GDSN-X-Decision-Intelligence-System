from sqlalchemy.orm import Session
from sqlalchemy import or_

from db import models
from auth.security import hash_password, verify_password


def create_user(db: Session, username: str, email: str, password: str):

    existing_user = db.query(models.User).filter(
        or_(
            models.User.username == username,
            models.User.email == email
        )
    ).first()

    if existing_user:
        return None

    hashed_password = hash_password(password)

    new_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        return None


def get_user(db: Session, username: str):

    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def verify_user(db: Session, username: str, password: str):

    user = get_user(db, username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def delete_user(db: Session, user_id: int):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return False

    try:
        db.delete(user)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
