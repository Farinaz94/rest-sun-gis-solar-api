from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import requests, jwt

router = APIRouter(tags=["Authentication"])
security = HTTPBasic()

ACTINIA_URL = "http://localhost:8088"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@router.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    # Step 1: Validate with Actinia
    token_url = f"{ACTINIA_URL}/api/v3/token"
    response = requests.get(token_url, auth=(credentials.username, credentials.password))
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Actinia credentials")

    # Step 2: Optional role logic
    token_data = {"sub": credentials.username}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

