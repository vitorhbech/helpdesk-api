from typing import Generator
from sqlalchemy.orm import Session
from app.models.database import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()