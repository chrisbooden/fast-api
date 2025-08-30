from fastapi import APIRouter, Request, HTTPException, status
from database import DBDependency
from models import Users
from routes.auth import UserDependency
from routes.utils.auth_util import generate_hash, verify_user
from pydantic import BaseModel, Field

router = APIRouter()

# Request Models
class UserRequest(BaseModel):
    user_name: str = Field(min_length=5, max_length=100)
    first_name:str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=5, max_length=50)

class PasswordRequest(BaseModel):
    password: str = Field(min_length=5, max_length=50)
    new_password: str = Field(min_length= 5, max_length=50)

# Create user
@router.post("/create-user")
def create_user(req: Request, user_data: UserRequest, db: DBDependency):
    user_dict = user_data.model_dump()
    user_dict["log_id"] = req.state.log_id
    user_dict["hashed_password"] = generate_hash(user_dict.get("password"))

    del user_dict["password"]

    db.add(Users(**user_dict))
    db.commit()

# Update details
@router.put("/update-password")
def create_user(req: Request, user_data: PasswordRequest, db: DBDependency, user: UserDependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    # Step 1: Validate password
    db_user = db.query(Users).filter(Users.user_id == user.get("user_id")).first()

    if not verify_user(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    if user_data.password == user_data.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot match old password")

    # Step 2: Set the new password and update the database
    db_user.hashed_password = generate_hash(user_data.new_password)
    db_user.log_id = req.state.log_id

    db.commit()
