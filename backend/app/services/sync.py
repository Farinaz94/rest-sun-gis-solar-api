from sqlalchemy.orm import Session
from app.models.user import User
from app.services.actinia.user_fetch import fetch_user_info
from datetime import datetime


def sync_user_profile(db: Session, username: str) -> User:
    """
    Sync user profile from Actinia to local PostgreSQL DB.
    Creates the user if not found. Updates role if user exists.
    """
    user_info = fetch_user_info(username)

    if not user_info:
        print(f"[Sync Error] Failed to fetch user data for '{username}' from Actinia.")
        return None

    # Use correct keys from Actinia response
    actinia_username = user_info.get("user_id")
    actinia_role = user_info.get("user_role")

    if not actinia_username or not actinia_role:
        print(f"[Sync Error] Missing expected keys in Actinia response: {user_info}")
        return None

    user = db.query(User).filter(User.username == actinia_username).first()

    if user:
        user.role = actinia_role
        db.commit()
        db.refresh(user)
        return user
    else:
        new_user = User(
            username=actinia_username,
            role=actinia_role,
            preferences="default"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

