from fastapi import APIRouter, HTTPException, Query
from starlette import status
from pydantic import BaseModel, Field
from routers.auth import user_dependency, hash_password, pwd_context
from database import db_dependency
from models import Users

router = APIRouter()

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get("/get-user", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    # Get the user
    db_user = db.query(Users).filter(Users.id == user.get("id")).first()  

    # Delete hashed password and return
    del db_user.hashed_password
    return db_user

@router.put("/change-password", status_code=status.HTTP_201_CREATED)
async def change_password(db: db_dependency, user: user_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")
    
    model_user = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if not pwd_context.verify(user_verification.password, model_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    model_user.hashed_password = pwd_context.hash(user_verification.new_password)
    db.commit()

    
