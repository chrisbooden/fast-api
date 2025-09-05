from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from routes.utils.auth_util import get_user, get_token, authorize_user 
from database import DBDependency

router = APIRouter()

# To inject into end points for authorization
UserDependency = Annotated[Session, Depends(get_user)]

# Request an access token
@router.post("/token")
def token(db: DBDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Authorize the user from the form data
    user = authorize_user(db, form_data.username, form_data.password)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not recognised")

    token = get_token(user.user_name, user.user_id)

    return {
        'access_token': token,
        "token_type": "bearer"
    }




