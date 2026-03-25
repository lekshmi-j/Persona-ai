from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.models.user import UserResponse
from app.services import user_service

# HTTPBearer tells FastAPI to look for:
# Authorization: Bearer <token>
# in the request header
bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> UserResponse:
    """
    FastAPI dependency — extracts and validates the JWT token.

    How it works:
    1. FastAPI extracts the Bearer token from the Authorization header
    2. We decode the token using our SECRET_KEY
    3. We extract the user_id from the token payload
    4. We look up the user in DynamoDB
    5. We return the user — or raise 401 if anything fails

    Usage in a route:
    @router.get("/")
    def my_route(current_user: UserResponse = Depends(get_current_user)):
        return current_user
    """

    # Reusable 401 error
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the token
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise credentials_exception

    # Extract user_id from payload
    # "sub" is the JWT standard field for the subject (user_id)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Look up user in DynamoDB
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user