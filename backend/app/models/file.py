from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, nullable=False)
    file_name: str = Field(index=True, nullable=False)
    uploaded_time: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return (
            f"File(id={self.id}, user_id={self.user_id}, "
            f"file_name='{self.file_name}', uploaded_time='{self.uploaded_time}')"
        )