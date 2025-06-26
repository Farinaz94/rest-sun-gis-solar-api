from sqlmodel import SQLModel, Field
from typing import Optional


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, nullable=False)
    job_name: str = Field(index=True, nullable=False)
    status: str = Field(index=True, nullable=False)

    def __repr__(self):
        return (
            f"job(id={self.id}, user_id={self.user_id}, "
            f"job_name='{self.job_name}', status='{self.status}')"
        )