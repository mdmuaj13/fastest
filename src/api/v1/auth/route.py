from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.utils.responser import ApiResponse
from src.utils.exceptions import ConflictException, UnauthorizedException
from src.utils.email import send_welcome_email
from .schema import SignupRequest, LoginRequest, UserResponse, AuthResponse
from .service import create_user, get_user_by_email, authenticate_user, generate_jwt_token, UserModel
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Register a new user.

    - Validates input (first_name, last_name, email, password)
    - Hashes the password with bcrypt
    - Returns 409 Conflict if email already exists
    - Returns JWT access token on success
    - Sends welcome email asynchronously
    """
    # Check for duplicate email
    existing_user = get_user_by_email(db, data.email)
    if existing_user:
        raise ConflictException(message="Email already registered")

    # Create user (password is hashed inside service)
    user = create_user(db, data)

    # Generate JWT token
    access_token = generate_jwt_token(user.id, user.email)

    # Send welcome email asynchronously
    # try:
    #     background_tasks.add_task(send_welcome_email, user.email)
    # except Exception as e:
    #     print(f"[EMAIL] Failed to queue welcome email: {str(e)}")

    return ApiResponse(
        data=AuthResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user),
        ).model_dump(),
        message="Registration successful",
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.

    - Validates email and password
    - Returns 401 if credentials are invalid
    - Returns JWT access token on success
    """
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise UnauthorizedException(message="Invalid email or password")

    access_token = generate_jwt_token(user.id, user.email)

    return ApiResponse(
        data=AuthResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user),
        ).model_dump(),
        message="Login successful",
    )


@router.get("/me")
def get_me(current_user: UserModel = Depends(get_current_user)):
    """
    Get the currently authenticated user's profile.
    Requires a valid JWT in the Authorization header.
    """
    return ApiResponse(
        data=UserResponse.model_validate(current_user).model_dump(),
        message="User retrieved successfully",
    )
