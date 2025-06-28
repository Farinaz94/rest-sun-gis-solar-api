from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# Set up the database engine using the URL from your settings
engine = create_engine(settings.DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is what FastAPI uses to inject db: Session into routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
