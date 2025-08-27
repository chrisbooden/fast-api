
from routers.auth import authorize_user, create_token, SECRET_KEY, ALGORITHM, get_current_user
from .utils import user, override_db
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException, status

def test_authorize_user(override_db):
    authorized_user = authorize_user(user["username"], 'abc123', override_db)
    assert authorized_user is not None
    assert authorized_user.username == user["username"]

    not_exists_user = authorize_user("wrong_user", "abc123", override_db)
    assert not_exists_user is None

    wrong_password = authorize_user(user["username"], 'abc1234', override_db)
    assert wrong_password is None

def test_create_access_token():
    username = "test_user" 
    user_id = 1
    role = "admin"
    expires_delta = timedelta(days=1)

    token = create_token(username, user_id, role, expires_delta)
    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decode_token["sub"] == username
    assert decode_token["id"] == user_id
    assert decode_token["role"] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {
        "sub": "test_user",
        "id": 1,
        "role": "admin"
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {
        "username": "test_user",
        "id": 1,
        "role": "admin"
    }

@pytest.mark.asyncio
async def test_get_current_user_invalid_payload():
    encode = {
        "role": "admin"
    }
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate credentials"
