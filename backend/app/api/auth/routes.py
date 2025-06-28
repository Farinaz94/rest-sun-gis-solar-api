from fastapi import APIRouter, HTTPException, status, Form, Depends
from app.services.actinia.validation import validate_actinia_user
from app.services.auth.jwt import create_access_token, refresh_token, verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db

router = APIRouter()

# Use HTTPBearer
http_bearer = HTTPBearer()

@router.get("/me")
def get_user_profile(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user_info = verify_token(token)
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    # NEW: fetch real user from DB
    user = db.query(User).filter(User.username == user_info["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.username,
        "role": user.role,
        "groups": user.groups
    }


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if not validate_actinia_user(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Actinia credentials")

    user_info = {
        "role": "user",
        "groups": ["solar_team"]
    }

    token = create_access_token(data={
        "sub": username,
        "role": user_info["role"],
        "groups": user_info["groups"]
    })

    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh")
def refresh_token_endpoint(token: str = Form(...)):
    new_token = refresh_token(token)
    if not new_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return {"access_token": new_token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Form(...)):
    return {"message": "User logged out successfully"}
