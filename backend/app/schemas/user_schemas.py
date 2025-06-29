from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    role: Optional[str] = None
    preferences: Optional[dict] = None
    groups: list[str]

    class Config:
        orm_mode = True

