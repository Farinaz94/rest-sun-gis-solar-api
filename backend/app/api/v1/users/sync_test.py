from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.sync import sync_user_profile
from  app.schemas.user_schemas import UserCreate, UserOut


router = APIRouter()

@router.post("/{username}")
def sync_user(username: str, db: Session = Depends(get_db)):
    user = sync_user_profile(db, username)

    if user:
        return {
            "message": f"User '{user.username}' synced successfully",
            "role": user.role
        }
    else:
        return {
            "message": f"Failed to sync user '{username}'"
        }

