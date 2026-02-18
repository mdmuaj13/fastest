from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.utils.exceptions import UnauthorizedException
from .service import verify_jwt_token, get_user_by_id
from src.models.user import UserModel

# Define the security scheme
security = HTTPBearer()


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserModel:
    """
    FastAPI dependency that extracts and verifies the JWT from the
    Authorization header using HTTPBearer security scheme.
    Returns the authenticated UserModel.
    """
    # HTTPBearer automatically checks for Authorization: Bearer <token>
    # and returns HTTPAuthorizationCredentials(scheme='Bearer', credentials='<token>')
    
    try:
        payload = verify_jwt_token(token.credentials)
    except Exception:
        raise UnauthorizedException(message="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException(message="Invalid token payload")

    user = get_user_by_id(db, int(user_id))
    if not user:
        raise UnauthorizedException(message="User not found")

    return user
