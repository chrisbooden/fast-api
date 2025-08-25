from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from starlette import status
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from typing import Annotated
from database import db_dependency
from models import Users

router = APIRouter()

SECRET_KEY = '7dc4ee24f66269bf8083a0439dc4f1abb3cb6e93d35a56650d994d84dc4a1347'
ALGORITHM = 'HS256'

class CreateUserRequest(BaseModel):
    username: str = Field(max_length=100)
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Set up passlib context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def hash_password(password: str) -> str:
    """Hash a plain password for storage."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def authorize_user(username: str, password: str, db: Session) -> Users:
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None    
    return user

def create_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {
            "username": username,
            "id": user_id,
            "role": role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

user_dependency = Annotated[Session, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    return db.query(Users).all()

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authorize_user(form_data.username, form_data.password, db)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    token = create_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {
        'access_token': token,
        "token_type": "bearer"
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user: CreateUserRequest):
    # Add the hashed password
    user = create_user.__dict__
    user["hashed_password"] = hash_password(create_user.password)
    
    # Remove the password attribute
    del user["password"]

    # Now create the user
    new_user = Users(**user)

    db.add(new_user)
    db.commit()
    



    