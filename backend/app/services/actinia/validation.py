import requests
from app.config import settings

def validate_actinia_user(username: str, password: str) -> bool:
    """
    Validate user credentials with Actinia by checking the /api/v3/locations endpoint.
    """
    try:
        # Changed the endpoint to /api/v3/locations (check with your Actinia version)
        response = requests.get(
            url=f"{settings.ACTINIA_URL}/api/v3/locations",  # Updated the URL to /api/v3/locations
            auth=(username, password),
            timeout=5
        )
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False
