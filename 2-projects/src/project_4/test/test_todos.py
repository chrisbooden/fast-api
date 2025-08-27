from sqlalchemy import text
from models import Base, Todos, Users
from starlette import status
from .utils import client, mock_user, test_todo, override_db


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

def test_read_one_authenticated(test_todo):
    response = client.get(f"/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": test_todo.title,
        "description": test_todo.description,
        "priority": test_todo.priority,
        "complete": test_todo.complete,
        "owner_id": test_todo.owner_id,
        "id": test_todo.id,  # if your API returns the id
    }

def test_read_one_authenticated_not_found():
    response = client.get(f"/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Todo not found"
    }

def test_create_todo(override_db):
    # Preparet a new request
    request_data = {
        "title": "New Todo",
        "description": "New todo description!",
        "priority": 5,
        "complete": False
    }

    response = client.post("/todo/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    model_todo = override_db.query(Todos).filter(Todos.title == "New Todo").first()
    db_data = {key: getattr(model_todo, key) for key in request_data.keys()}
    
    assert db_data == request_data

    # Clear the table after the test
    override_db.query(Todos).delete()
    override_db.commit()

def test_update_todo(override_db):
    request_data = {
        "title": "New Todos",
        "description": "Need to learn every day",
        "priority": 5,
        "complete": False
    }

    todo = Todos(**request_data, owner_id=mock_user()["id"])
    override_db.add(todo)
    override_db.commit()

    # Update a field
    request_data["title"] = "Updated Todo"

    response = client.put(f"/todo/{todo.id}", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Need to refresh the sqlalchemy cache
    override_db.refresh(todo)

    # Check the updated todo matches the updated data
    db_data = { key: getattr(todo, key) for key in request_data.keys() }
    print(db_data)
    assert request_data == db_data

    # Clear the table after the test
    override_db.query(Todos).delete()
    override_db.commit()

def test_update_todo_not_found():
    request_data = {
        "title": "New Todos",
        "description": "Need to learn every day",
        "priority": 5,
        "complete": False
    }

    response = client.put(f"/todo/9999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == { "detail": "Todo not found" }

def test_delete_todo(test_todo, override_db):
    response = client.delete(f"/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    model = override_db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None

def test_delete_todo_not_found():
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    