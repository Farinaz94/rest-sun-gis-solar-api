from fastapi import FastAPI
from app.api.auth.routes import router as auth_router
from app.api.v1.users import router as user_router
from app.api.v1.users.profile_routes import router as profile_router
from app.services.auth.permissions import require_role
from app.api.upload import routes as upload_routes




app = FastAPI(title="FastAPI App is running")




@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI backend!"}


# Register the routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["User Management"])
app.include_router(profile_router, prefix="/profile", tags=["User Profile"])
app.include_router(upload_routes.router, prefix="/upload", tags=["Upload"])



