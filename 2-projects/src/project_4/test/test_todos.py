from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from routers.auth import get_current_user
from database import get_db
from models import Base, Todos, Users
from starlette import status
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
    return {
        "username": "test_user",
        "id": 1,
        "user_role": "admin"
    }

# Override the get_db to the testing db
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = mock_user

# Mock the app for testing
client = TestClient(app)

@fixture
def test_session(override_db):

    # Check that we have the test user present    
    db_user = override_db.query(Users).filter(Users.username=="test_user").first()
    
    if not db_user:
        model_user = Users(
            email="test@test.com",
            username="test_user",
            first_name="admin",
            last_name="test",
            hashed_password="abc123",
            is_active=True,
            role="admin"
        )
        override_db.add(model_user)  
        override_db.commit()  # save changes to commit a user   


@fixture
def test_todo(override_db):
    # Add a todo to the database
    todo = Todos(
        title="Learn to code",
        description="Need to learn every day",
        priority=5,
        complete=False,
        owner_id=1
    )

    override_db.add(todo)
    override_db.flush() # send pending changes

    # Return the todo
    yield todo

    # Cleanup after 
    override_db.rollback() # remove any changes in the test

def test_read_all_authenticated(test_todo):
    response = client.get("/todo/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "title": test_todo.title,
        "description": test_todo.description,
        "priority": test_todo.priority,
        "complete": test_todo.complete,
        "owner_id": test_todo.owner_id,
        "id": test_todo.id,  # if your API returns the id
    }]

