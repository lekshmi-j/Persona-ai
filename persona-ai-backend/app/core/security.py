from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# CryptContext tells passlib to use bcrypt algorithm
# deprecated="auto" means old hashes get upgraded automatically
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Turns plain text password into a bcrypt hash.
    Example: "mypassword" → "$2b$12$abc123..."
    This process is one-way — you can never reverse it back.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain password matches a stored hash.
    Used during login to verify the user's password.
    Returns True if match, False if not.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a signed JWT token containing the provided data.
    The token expires after ACCESS_TOKEN_EXPIRE_MINUTES by default.

    data should contain: {"sub": user_id}
    "sub" is JWT standard for "subject" — who this token is about.
    """
    to_encode = data.copy()

    # Set expiry time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    # Sign the token with our SECRET_KEY
    # Only someone with the SECRET_KEY can verify this token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes and verifies a JWT token.
    Returns the payload dict if valid.
    Returns None if token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None