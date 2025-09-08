from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..core.security import (
    UserCredentials,
    authenticate_user,
    register_user,
    issue_token_for_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


class AuthResponse(BaseModel):
    """Token response payload including a basic message."""
    token: str = Field(..., description="Bearer token to authenticate subsequent requests.")
    message: str = Field(..., description="Human readable status message.")


@router.post(
    "/register",
    summary="Register a new user",
    response_model=AuthResponse,
    responses={
        400: {"description": "User already exists."},
    },
)
def register(creds: UserCredentials):
    """
    Register a new account with email and password and receive a token.

    Parameters:
        - creds: UserCredentials containing email and password.

    Returns:
        AuthResponse with token and message.
    """
    user_id = register_user(creds.email, creds.password)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    token = issue_token_for_user(user_id)
    return AuthResponse(token=token, message="Registration successful")


@router.post(
    "/login",
    summary="Login user",
    response_model=AuthResponse,
    responses={
        401: {"description": "Invalid credentials."},
    },
)
def login(creds: UserCredentials):
    """
    Login using email and password to receive a token.

    Parameters:
        - creds: UserCredentials containing email and password.

    Returns:
        AuthResponse with token and message.
    """
    user_id = authenticate_user(creds.email, creds.password)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = issue_token_for_user(user_id)
    return AuthResponse(token=token, message="Login successful")
