from fastapi import APIRouter, HTTPException, status, Form, Depends
from app.services.actinia.validation import validate_actinia_user
from app.services.auth.jwt import create_access_token, refresh_token, verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from fastapi import Request
from app.models import user, Session as SessionModel
from datetime import datetime
from app.models import Session
import uuid
from jose import jwt, JWTError
from app.config import settings
from app.services.auth.permissions import require_role
from uuid import uuid4  

router = APIRouter()
  
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
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Step 1: Validate credentials
    if not validate_actinia_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid Actinia credentials")

    # Step 2: Find user (before creating token!)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 3: Generate token using user's actual role and groups
    # Inside your /login route
    token = create_access_token({
        "sub": username,
        "user_id": user.id,
        "username": user.username, 
        "role": user.role,
        "groups": user.groups or []
    })



    # Step 4: Extract metadata
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")

    # Step 5: Store session
    session = SessionModel(
        user_id=user.id,
        session_token=token,
        ip_address=ip,
        user_agent=user_agent,
        is_active=True,
        login_time=datetime.utcnow()
    )
    db.add(session)
    db.commit()

    return {"access_token": token, "token_type": "bearer"}


@router.get("/ip_address")
def get_ip_address(request: Request):
    return {"ip_address": request.client.host}


@router.post("/refresh")
def refresh_token_endpoint(token: str = Form(...)):
    new_token = refresh_token(token)
    if not new_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    token = credentials.credentials 

    session = db.query(SessionModel).filter_by(session_token=token, is_active=True).first()
    if not session:
        raise HTTPException(status_code=404, detail="Active session not found")

    session.is_active = False
    session.logout_time = datetime.utcnow()
    db.commit()

    return {"message": "User logged out successfully"}

@router.get("/admin-panel")
def get_admin_data(current_user=Depends(require_role(["admin"]))):
    return {"msg": f"Welcome, admin {current_user.username}!"}
