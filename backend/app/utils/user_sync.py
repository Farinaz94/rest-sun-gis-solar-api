import requests
from sqlalchemy.orm import Session
from app.models import User  # adjust import if path is different
from app.schemas import UserCreate  # if you use Pydantic schema for creation

ACTINIA_BASE_URL = "http://localhost:8088"

def sync_user_from_actinia(token: str, db: Session) -> User:
    """
    Fetch user info from Actinia and sync it with our database.
    Returns the synced User object.
    """

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{ACTINIA_BASE_URL}/whoami", headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise Exception(f"Failed to contact Actinia: {e}")

    username = data.get("user")
    roles = data.get("roles", [])  # example: ["admin", "user"]

    if not username:
        raise Exception("Invalid user info received from Actinia.")

    # Check if the user already exists
    user = db.query(User).filter(User.username == username).first()

    if not user:
        # Create new user
        user = User(username=username, roles=",".join(roles))
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Optional: update roles if they changed
        current_roles = set(user.roles.split(","))
        new_roles = set(roles)
        if current_roles != new_roles:
            user.roles = ",".join(roles)
            db.commit()

    return user
