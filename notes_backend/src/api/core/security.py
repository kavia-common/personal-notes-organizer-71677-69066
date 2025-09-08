"""
Security utilities and dependencies for token-based authentication.
This uses an in-memory, mock authentication strategy for demo purposes.
"""
from typing import Optional, Dict
from fastapi import Header, HTTPException, status
from pydantic import BaseModel, Field


# Simple in-memory user store and token store (mock)
_USERS = {
    # username: {"id": user_id, "password": "plain-text-pw-for-demo"}
    "alice@example.com": {"id": "user_1", "password": "password123"},
    "bob@example.com": {"id": "user_2", "password": "hunter2"},
}

_TOKENS: Dict[str, str] = {}  # token -> user_id


class TokenData(BaseModel):
    """Represents an auth token returned by login/register."""
    token: str = Field(..., description="Bearer token to authenticate subsequent requests.")


class UserCredentials(BaseModel):
    """User credentials for login/register requests."""
    email: str = Field(..., description="User email (used as username).")
    password: str = Field(..., min_length=6, description="Plain-text password for demo purposes.")


# PUBLIC_INTERFACE
def issue_token_for_user(user_id: str) -> str:
    """Issue a pseudo-random token for a given user id and store it in-memory."""
    import secrets
    token = secrets.token_urlsafe(32)
    _TOKENS[token] = user_id
    return token


# PUBLIC_INTERFACE
def authenticate_user(email: str, password: str) -> Optional[str]:
    """Authenticate given credentials. Returns user_id if valid, else None."""
    record = _USERS.get(email)
    if not record:
        return None
    if record["password"] != password:
        return None
    return record["id"]


# PUBLIC_INTERFACE
def register_user(email: str, password: str) -> Optional[str]:
    """Register new user if it doesn't exist. Returns user_id on success, None if exists."""
    if email in _USERS:
        return None
    new_id = f"user_{len(_USERS) + 1}"
    _USERS[email] = {"id": new_id, "password": password}
    return new_id


# PUBLIC_INTERFACE
def get_current_user_id(authorization: Optional[str] = Header(default=None)) -> str:
    """
    FastAPI dependency to get current user_id from Authorization header.

    Accepts:
        Authorization: 'Bearer <token>'

    Returns:
        user_id (str)

    Raises:
        HTTPException 401 if header/token invalid.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected: 'Bearer <token>'",
        )
    token = parts[1]
    user_id = _TOKENS.get(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return user_id
