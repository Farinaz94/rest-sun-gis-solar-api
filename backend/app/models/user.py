from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    preferences: Optional[str] = Field(index=True, unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


    def __repr__(self):
        return (
            f"User(id={self.id}, username='{self.username}', "
            f"preferences='{self.preferences}', created_at='{self.created_at}')"
        )