import requests
from requests.auth import HTTPBasicAuth
from app.config import settings

def fetch_user_info(username: str):
    try:
        response = requests.get(
            f"{settings.ACTINIA_URL}/api/v3/users/{username}",
            auth=HTTPBasicAuth(settings.ACTINIA_USER, settings.ACTINIA_PASSWORD)
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[Sync Error] Failed to fetch user data for '{username}' from Actinia.")
            print(f"[Status] {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"[Exception] {e}")
        return None

