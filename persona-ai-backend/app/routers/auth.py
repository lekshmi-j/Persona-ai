from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, status
from app.models.user import UserCreate, UserResponse
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.services import user_service
from app.core.limiter import limiter

router = APIRouter()

@router.post("/register", response_model=UserResponse,
             status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register(request: Request, user_data: UserCreate):
    """
    Creates a new user account.

    Steps:
    1. Check email not already registered
    2. Hash the password
    3. Store user in DynamoDB
    4. Return user info (no password)

    Rate limited to 3 registrations per minute per IP.
    """
    # Check email not already taken
    if user_service.email_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create and return the user
    return user_service.create_user(user_data)


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, user_data: UserCreate):
    """
    Authenticates a user and returns a JWT token.

    Steps:
    1. Find user by email in DynamoDB
    2. Verify password against stored hash
    3. Create a signed JWT token
    4. Return the token

    Rate limited to 5 login attempts per minute per IP.
    """
    # Find user by email
    user = user_service.get_user_by_email(user_data.email)

    # Verify password — same error message whether email or
    # password is wrong (security best practice — don't reveal
    # which one failed)
    if not user or not verify_password(user_data.password,
                                       user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token — "sub" contains the user_id
    access_token = create_access_token(
        data={"sub": user.user_id},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }