# Set sys path appropriately for python module imports to work
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from routers.auth import get_current_user
from database import get_db
from models import Base, Todos, Users
from routers.auth import pwd_context 
from pytest import fixture

# Testing db
SQL_ALCHEMY_DATABASE_URL = 'postgresql://admin:password@localhost:5433/testdb_todos'

# Create and handle connections via an engine
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, poolclass=StaticPool)

# Create Local session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create db and structure
Base.metadata.create_all(bind=engine)

# Create a db connection and finally close
def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

# Fixture version to call when using the connection in a test
@fixture
def override_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

# Mock a fake user
def mock_user():
    # Check that we have the test user present 
    db = TestingSessionLocal()

    db_user = db.query(Users).filter(Users.username=="test_user").first()
    
    if not db_user:
        model_user = Users(
            email="test@test.com",
            username="test_user",
            first_name="admin",
            last_name="test",
            hashed_password=pwd_context.hash("abc123"),
            is_active=True,
            role="admin"
        )
        db.add(model_user)  
        db.commit()  # save changes to commit a user   

        return {
            "username": model_user.username,
            "id": model_user.id,
            "role": model_user.role
        }

    db.close()

    return {
        "username": db_user.username,
        "id": db_user.id,
        "role": db_user.role
    }

# Add the user to the db first
user = mock_user()

# Override the get_db to the testing db
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = mock_user

# Mock the app for testing
client = TestClient(app)  

@fixture
def test_todo(override_db):
    # Add a todo to the database
    todo = Todos(
        title="Learn to code",
        description="Need to learn every days",
        priority=5,
        complete=False,
        owner_id=user["id"]
    )

    override_db.add(todo)
    override_db.commit() # send pending changes

    # Return the todo
    yield todo

    override_db.query(Todos).delete()
    override_db.commit()
    override_db.close()

# @fixture
# def test_user(override_db):
#     user = Users(
#         username="test_user",
#         email="test@test.com",
#         first_name="admin",
#         last_name="test",
#         hashed_password=pwd_context.hash("abc123"),
#         is_active=True,
#         role="admin"
#     )

#     override_db.add(user)
#     override_db.flush()

#     yield user

#     override_db.rollback()