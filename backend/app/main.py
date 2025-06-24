from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from app.routes.login import router as login_router
from app.routes.auth import router as auth_router

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="Bearer")


# Register routers
app.include_router(login_router)              # /auth/login
app.include_router(auth_router, prefix="/auth")  # /auth/me, /auth/refresh...

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI app!"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI App",
        version="1.0.0",
        description="REST API with JWT Authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
