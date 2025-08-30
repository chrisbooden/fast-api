from fastapi import FastAPI
from routes import auth, todos, users
from middleware import logging

app = FastAPI()

# Add middleware
app.middleware("http")(logging.logger)

# Add routes
app.include_router(prefix="/auth", tags=["auth"], router=auth.router)
app.include_router(prefix="/users", tags=["users"], router=users.router)
app.include_router(prefix="/todos", tags=["todos"], router=todos.router)

@app.get("/health-check")
def health_check():
    return {
        "detail": "FastAPI healthy"
    }