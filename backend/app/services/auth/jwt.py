from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import ExpiredSignatureError
from app.models import Session as UserSession 

# OAuth2PasswordBearer is used for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
# Use HTTPBearer instead of OAuth2PasswordBearer for cleaner Swagger UI
oauth2_scheme = HTTPBearer()


# Extracts and verifies JWT token, returns the current user from the database
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Token payload invalid", headers={"WWW-Authenticate": "Bearer"}
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"}
        )

    # Validate user existence
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=401, detail="User not found", headers={"WWW-Authenticate": "Bearer"}
        )

    # 🔐 Check session status
    session = db.query(UserSession).filter(UserSession.session_token == token).first()
    if session is None or not session.is_active or session.invalidated_by_admin:
        raise HTTPException(
            status_code=401,
            detail="Session is no longer active or was invalidated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


# JWT Token Generation
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# JWT Token Validation
def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload if payload["exp"] >= datetime.utcnow().timestamp() else None
    except JWTError:
        return None

# Refresh Token
def refresh_token(token: str) -> str | None:
    payload = verify_token(token)
    if payload is None:
        return None
    return create_access_token(data=payload, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
