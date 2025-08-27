# # Set sys path appropriately for python module imports to work
from starlette import status
from .utils import override_db, client, test_todo
from models import Todos


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/")

    assert response.status_code == status.HTTP_200_OK
    db_dict = response.json().pop()
    test_dict = { key: getattr(test_todo, key) for key in db_dict.keys() }
    assert db_dict == test_dict


def test_admin_delete_todo(test_todo, override_db):
    response = client.delete(f"/admin/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    todo = override_db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert todo is None

def test_admin_delete_todo_not_found():
    response = client.delete(f"/admin/todo/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == { "detail": "Todo not found" }



