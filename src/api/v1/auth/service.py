import os
from datetime import datetime, timezone, timedelta
from typing import Optional

import bcrypt
import jwt

from .schema import SignupRequest


# ─── Configuration ───────────────────────────────────────────────────────────

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))



# ─── Password Utilities ─────────────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ─── JWT Utilities ───────────────────────────────────────────────────────────

def generate_jwt_token(user_id: int, email: str) -> str:
    """Generate a JWT access token for the given user."""
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises jwt.PyJWTError on failure."""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


# ─── Service Functions ───────────────────────────────────────────────────────

def get_user_by_email(db, email: str) -> Optional[UserModel]:
    """Find a user by email address."""
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_id(db, user_id: int) -> Optional[UserModel]:
    """Find a user by ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def create_user(db, data: SignupRequest) -> UserModel:
    """Create a new user with a hashed password."""
    db_user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=hash_password(data.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db, email: str, password: str) -> Optional[UserModel]:
    """Authenticate a user by email and password. Returns the user or None."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
