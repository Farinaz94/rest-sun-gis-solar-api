from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings

# JWT Token Generation

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token with claims and expiration.
    - data: the payload (e.g., user info, role)
    - expires_delta: custom expiration time (optional, defaults to 30 minutes)
    """
    to_encode = data.copy()  # Copy the data, so we don’t mutate the original
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))  # Use UTC time correctly
    to_encode.update({"exp": expire})  # Add expiration to the token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# JWT Token Validation
def verify_token(token: str) -> dict | None:
    """
    Verify and decode the JWT token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload if payload["exp"] >= datetime.utcnow().timestamp() else None
    except JWTError:
        return None


# Optional: Refresh Token (create a new token with a fresh expiration)
def refresh_token(token: str) -> str | None:
    """
    Refresh the JWT token (issue a new token with a new expiration)
    """
    payload = verify_token(token)
    if payload is None:
        return None  # If the old token is invalid or expired, return None
    
    # Create a new token with extended expiration
    return create_access_token(data=payload, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
