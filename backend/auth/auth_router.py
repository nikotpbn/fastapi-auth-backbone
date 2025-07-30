from datetime import datetime, timedelta
from typing import Annotated

from bson.objectid import ObjectId

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .serializers import UserSerializer, Token
from ..dependencies import (
    database_connect,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()


@router.post("/login/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    client=Depends(database_connect),
):
    """
    OAuth2 specs require a form data with username and password.
    In this case username is email, thus data is transported as username
    but it contains email.
    """
    user = await authenticate_user(client, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/user/")
async def user_create(user: UserSerializer, client=Depends(database_connect)):
    payload = user.model_dump()
    if "id" in payload:
        id = payload.pop("id")
        payload["_id"] = ObjectId(id)

    payload["password"] = get_password_hash(payload["password"])

    result = await client.auth.users.insert_one(payload)

    return {
        "message": "User created successfully",
        "user_id": str(result.inserted_id),
    }

@router.get("/user/me/")
async def get_current_user(current_user: Annotated[UserSerializer, Depends(get_current_user)]):
    return current_user


@router.get("/user/{user_id}")
async def user_detail(user_id: str, client=Depends(database_connect)):
    result = await client.auth.users.find_one({"_id": ObjectId(user_id)})

    if result:
        result["_id"] = str(result["_id"])
        return result

    return {"message": "User not found"}


@router.put("/user/{user_id}")
async def user_update(
    user_id: str, user: UserSerializer, client=Depends(database_connect)
):
    update = {"$set": user.model_dump()}

    response = await client.auth.users.update_one({"_id": ObjectId(user_id)}, update)

    if response.matched_count > 0:
        return {"message": "User updated successfully"}

    return {"message": "User not found"}


@router.delete("/user/{user_id}")
async def user_delete(user_id: str, client=Depends(database_connect)):
    result = await client.auth.users.delete_one({"_id": ObjectId(user_id)})

    return {"message": "User deleted successfully"}
