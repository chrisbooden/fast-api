from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from typing import Dict, Annotated
from models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Decodes a JWT token and returns user information.

    Args:
        token (str): The JWT token to decode.

    Returns:
        Dict: A dictionary with user_name, user_id, and role.

    Raises:
        HTTPException: If the token is invalid or user is unauthorized.
    """
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get("sub"),
        user_id = payload.get('id'),
        role = payload.get("role")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User unauthorized")
    
        return {
            "user_name": user_name,
            "user_id": user_id,
            "role": role
        }
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

def get_token(user_name: str, user_id: int, role: str) -> str:
    """
    Returns a JWT for a user claim

    Args:
        user_name (str): The user name to encode
        user_id (int): The user id to encode
        role (str): The user role to encode

    Returns
        str: A jason web token
    """
    encode = {
        "sub": user_name,
        "id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(claims=encode,key=SECRET_KEY,algorithm=ALGORITHM)

def generate_hash(password: str) -> str:
    """
    Generated an HS256 hash of a string
    """
    return pwd_context.hash(password)

def verify_user(password: str, hashed_password: str) -> bool:
    """
    Verifies if a password matches a stored hashed password

    Args:
        password (str): The user password
        hashed_password (str): The stored hashed_password

    Returns:
        bool: True if they match, false if not 
    """

    return pwd_context.verify(secret=password, hash=hashed_password)

def authorize_user(db: Session, user_name: str, password: str) -> Users:
    """
    Returns a user given the user's user_name and password

    Args:
        db (Session): The database session to query for user info
        user_name (str): The user name for a user
        password (str): The password for the user
    Returns
        A single user of class Users from the backend db
    """

    user = db.query(Users).filter(Users.user_name == user_name).first()

    if not user:
        return None
    
    if not verify_user(password, user.hashed_password):
        return None
    
    return user


