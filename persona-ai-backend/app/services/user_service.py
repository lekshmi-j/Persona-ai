import uuid
from datetime import datetime
from typing import Optional
from app.models.user import UserCreate, UserResponse, UserInDB
from app.core.security import hash_password
from app.services.dynamodb import put_item, get_item, list_items
import logging

logger = logging.getLogger(__name__)

TABLE_NAME = "Users"

def create_user(user_data: UserCreate) -> UserResponse:
    """
    Creates a new user in DynamoDB.
    Hashes the password before storing — never stores plain text.
    Returns UserResponse (no password field).
    """
    user_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    # Build the item to store in DynamoDB
    user_item = {
        "user_id": user_id,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "created_at": now,
        "is_active": True,
    }

    put_item(TABLE_NAME, user_item)
    logger.info(f"Created user: {user_id}")

    # Return UserResponse — no password field
    return UserResponse(
        user_id=user_id,
        email=user_data.email,
        created_at=now,
        is_active=True,
    )

def get_user_by_email(email: str) -> Optional[UserInDB]:
    """
    Finds a user by email address.
    Used during login to verify credentials.
    Returns UserInDB which includes hashed_password for verification.
    Returns None if not found.

    Note: This uses a scan — not ideal for large tables.
    In production you'd add a Global Secondary Index (GSI)
    on email for faster lookups. Fine for now.
    """
    users = list_items(TABLE_NAME)
    for user in users:
        if user.get("email") == email:
            return UserInDB(
                user_id=user["user_id"],
                email=user["email"],
                hashed_password=user["hashed_password"],
                created_at=user["created_at"],
                is_active=user.get("is_active", True),
            )
    return None

def get_user_by_id(user_id: str) -> Optional[UserResponse]:
    """
    Finds a user by their user_id partition key.
    Used by get_current_user dependency to load user from token.
    Returns UserResponse (no password).
    Returns None if not found.
    """
    user = get_item(TABLE_NAME, {"user_id": user_id})
    if not user:
        return None

    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        created_at=user["created_at"],
        is_active=user.get("is_active", True),
    )

def email_exists(email: str) -> bool:
    """
    Checks if an email is already registered.
    Used during registration to prevent duplicate accounts.
    """
    return get_user_by_email(email) is not None