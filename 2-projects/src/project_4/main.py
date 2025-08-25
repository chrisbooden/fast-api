from fastapi import FastAPI
from routers import auth, todos, admin, users

app = FastAPI()

app.include_router(prefix="/auth", tags=["auth"], router=auth.router)
app.include_router(prefix="/todo", tags=["todo"], router=todos.router)
app.include_router(prefix="/admin", tags=["admin"], router=admin.router)
app.include_router(prefix="/users", tags=["users"], router=users.router)






