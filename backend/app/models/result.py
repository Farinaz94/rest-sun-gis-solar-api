from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, nullable=False)
    job_id: int = Field(index=True, nullable=False)
    file_name: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sharing_permission: str = Field(default="private", nullable=False)
    

    def __repr__(self):
        return (
            f"Result(id={self.id}, user_id={self.user_id}, "
            f"job_id='{self.job_id}', file_name='{self.file_name}')"
        )