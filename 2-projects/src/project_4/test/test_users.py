# # Set sys path appropriately for python module imports to work
from starlette import status
from .utils import client
from models import Todos, Users

def test_return_user():
    response = client.get("/users/get-user")
    assert response.status_code == status.HTTP_200_OK

def test_change_password():
    data = {
        "password": "abc123",
        "new_password": "abc123"
    }
    response = client.put("/users/change-password", json=data)
    assert response.status_code == status.HTTP_201_CREATED

def test_change_invalid_password():
    data = {
        "password": "abc1234",
        "new_password": "abc123"
    }
    response = client.put("/users/change-password", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED   
    assert response.json() == { "detail": "Incorrect password" }