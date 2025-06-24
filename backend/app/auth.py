from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

from app.schemas import Token, User
from app.services.auth import create_access_token, get_current_active_user
import requests
import os

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Load Actinia URL from env
ACTINIA_URL = os.getenv("ACTINIA_URL", "http://localhost:8088/api/v3/locations")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        response = requests.get(
            ACTINIA_URL,
            auth=(form_data.username, form_data.password),
            timeout=5
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Actinia credentials"
            )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Actinia not reachable: {str(e)}"
        )

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def get_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.post("/logout")
async def logout():
    # Placeholder: In JWT, logout is stateless unless you store token blacklist
    return {"message": "Logout endpoint hit. In JWT, implement blacklist to invalidate token."}


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    # This would typically use refresh tokens (not implemented here)
    new_token = create_access_token(data={"sub": current_user.username})
    return {"access_token": new_token, "token_type": "bearer"}

