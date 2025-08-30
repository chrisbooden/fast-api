from fastapi import Request, APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from database import DBDependency
from routes.auth import UserDependency
from models import Todos

router = APIRouter()

# Request Models
class TodoRequest(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    completed: bool

# Get all todos - for a user
@router.get("/")
def get_all_todos(db: DBDependency, user: UserDependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    todos = db.query(Todos).filter(Todos.user_id == user.get("user_id")).all()

    return todos

# Get a single todod by id
@router.get("/{todo_id}/")
def get_todo(db: DBDependency, user: UserDependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    todo = db.query(Todos).filter(Todos.user_id == user.get("user_id")).filter(Todos.todo_id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    return todo

# Create todo
@router.post("/create-todo")
def create_todo(req: Request, db: DBDependency, user: UserDependency, todo: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    todo_dict = todo.model_dump()
    todo_dict["log_id"] = req.state.log_id
    todo_dict["user_id"] = user.get("user_id")

    db.add(Todos(**todo_dict))
    db.commit()

# Update todo
@router.put("/update-todo/{todo_id}")
def update_todo(req: Request, db: DBDependency, user: UserDependency, todo: TodoRequest, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    db_todo = db.query(Todos).filter(Todos.todo_id == todo_id).filter(Todos.user_id == user.get("user_id")).first()

    if db_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    # Update values and commit
    todo_dict = todo.model_dump()
    todo_dict["log_id"] = req.state.log_id
    todo_dict["user_id"] = user.get("user_id")

    db_todo.log_id = req.state.log_id
    
    for key, value in todo_dict.items():
        setattr(db_todo, key, value)

    db.commit()

# Delete a todo
@router.delete("/delete/{todo_id}")
def delete_todo(req: Request, db: DBDependency, user: UserDependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    todo = db.query(Todos).filter(Todos.todo_id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    db.query(Todos).filter(Todos.todo_id == todo_id).delete()
    db.commit()