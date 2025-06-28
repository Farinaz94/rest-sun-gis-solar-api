from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    role: str = Field(default="user", index=True, nullable=False)

    preferences: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        sa_column=Column(JSON)
    )

    groups: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )

    def __repr__(self):
        return (
            f"User(id={self.id}, username='{self.username}', "
            f"preferences={self.preferences})"
        )
