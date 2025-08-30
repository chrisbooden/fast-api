from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from models import Base
from config import SQL_ALCHEMY_URL

# Requests connection from an underlying pool
engine = create_engine(url=SQL_ALCHEMY_URL)

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database structure if empty
Base.metadata.create_all(bind=engine)

# Handle database connections
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Used to Inject db connection into our endpoints
DBDependency = Annotated[Session, Depends(get_db)]