from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User
from app.schemas.user_schemas import UserOut, UserUpdate
from app.services.auth.jwt import get_current_user


router = APIRouter(prefix="", tags=["User Profile"])

# Get current user profile
@router.get("/me", response_model=UserOut)
def read_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user

# Update current user profile
@router.put("/me", response_model=UserOut)
def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.username = user_update.username or current_user.username
    db.commit()
    db.refresh(current_user)
    return current_user

# Delete current user profile
@router.delete("/me")
def delete_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.delete(current_user)
    db.commit()
    return {"message": "User profile deleted successfully"}

# Update user preferences (example: language, theme, etc.)
@router.put("/me/preferences")
def update_preferences(
    preferences: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.preferences = preferences
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"message": "Preferences updated", "preferences": current_user.preferences}

# Update other account settings (placeholder)
@router.put("/me/settings")
def update_account_settings(
    settings: dict,
    current_user: User = Depends(get_current_user)
):
    return {
        "message": f"Account settings update received for user {current_user.username}.",
        "received": settings
    }


