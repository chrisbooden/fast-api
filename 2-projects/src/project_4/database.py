from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from sqlalchemy.orm import session
from models import Base

SQLALCHEMY_DATABASE_URL = 'postgresql://admin:password@localhost:5432/db_todos'

# Create and handle connections via engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database and structure
Base.metadata.create_all(bind=engine)

# Ensure connections are closed after data returned to the client
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Annotate the type session with the get all function.
# Fast api will then inject the value from get_db creating a new session each time.
db_dependency = Annotated[session, Depends(get_db)]