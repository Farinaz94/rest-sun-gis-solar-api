from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.utils.user_sync import sync_user_from_actinia


router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@router.get("/me")
def get_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        user = sync_user_from_actinia(token, db)
        return {
            "username": user.username,
            "role": user.role,
            "email": user.email
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User sync failed: {str(e)}")


@router.post("/refresh")
def refresh_token():
    return {"message": "Refresh token logic here"}

@router.post("/logout")
def logout():
    return {"message": "User logged out"}

