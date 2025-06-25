from fastapi import FastAPI
from app.api.auth.routes import router as auth_router  # Import the auth router

app = FastAPI(title="My First FastAPI App")

@app.get("/")
def root():
    return {"message": "Hello, FastAPI is working!"}

# Register the /auth routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
