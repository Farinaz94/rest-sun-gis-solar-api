from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, nullable=False)
    session_token: str = Field(index=True, unique=True, nullable=False)
    login_time: datetime = Field(default_factory=datetime.utcnow)
    logout_time: Optional[datetime] = Field(default=None, nullable=True)

    def __repr__(self):
        return (
            f"Session(id={self.id}, user_id={self.user_id}, "
            f"session_token='{self.session_token}', login_time='{self.login_time}', logout_time='{self.logout_time}')"
        )