from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from app.models.session import Session

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, nullable=False)
    file_name: str = Field(index=True, nullable=False)
    uploaded_time: datetime = Field(default_factory=datetime.utcnow)

    # Metadata fields
    file_type: Optional[str] = Field(default=None)   # "raster" or "vector"
    format: Optional[str] = Field(default=None)      # "tif", "zip", etc.
    epsg: Optional[int] = Field(default=None)        # e.g., 4326
    valid: bool = Field(default=True)                # set to False if validation fails

    # step2: GRASS metadata
    location: Optional[str] = Field(default=None)
    mapset: Optional[str] = Field(default=None)
    session_id: Optional[int] = Field(default=None, foreign_key="session.id")
    
    def __repr__(self):
        return (
            f"File(id={self.id}, user_id={self.user_id}, "
            f"file_name='{self.file_name}', epsg={self.epsg}, "
            f"file_type='{self.file_type}', format='{self.format}', "
            f"location='{self.location}', mapset='{self.mapset}', "
            f"valid={self.valid}, uploaded_time='{self.uploaded_time}')"
        )
