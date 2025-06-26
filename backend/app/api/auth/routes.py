from fastapi import APIRouter, HTTPException, status, Form, Depends 
from app.services.actinia.validation import validate_actinia_user  # Only import validate_actinia_user
from app.services.auth.jwt import create_access_token, refresh_token, verify_token
from fastapi.security import OAuth2PasswordBearer  # OAuth2PasswordBearer for token extraction

router = APIRouter()

# OAuth2PasswordBearer is used to get the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# The /auth/login endpoint to generate the JWT token
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    # Step 1: Validate Actinia credentials
    if not validate_actinia_user(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Actinia credentials")

    # Step 2: Get user information (role, groups, etc.)
    user_info = {
        "role": "user",  # Replace with actual logic or database call
        "groups": ["solar_team"]  # Replace with actual logic or database call
    }

    if not user_info.get("role") or not user_info.get("groups"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to fetch user info or roles")

    # Step 3: Generate JWT token with additional claims (e.g., role, groups)
    token = create_access_token(data={"sub": username, "role": user_info.get("role"), "groups": user_info.get("groups")})

    return {"access_token": token, "token_type": "bearer"}


# The /auth/refresh endpoint to refresh the JWT token
@router.post("/refresh")
def refresh_token_endpoint(token: str = Form(...)):
    # Step 1: Verify the current token and refresh it
    new_token = refresh_token(token)
    if not new_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return {"access_token": new_token, "token_type": "bearer"}

# The /auth/me endpoint to retrieve the user profile
@router.get("/me")
def get_user_profile(token: str = Depends(oauth2_scheme)):  # Now using Depends to extract the token
    user_info = verify_token(token)  # Verify the token and get the payload
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Return the user profile (could include more details as needed)
    return {"user_id": user_info["sub"], "role": user_info["role"], "groups": user_info["groups"]}

# The /auth/logout endpoint
@router.post("/logout")
def logout(token: str = Form(...)):
    return {"message": "User logged out successfully"}

