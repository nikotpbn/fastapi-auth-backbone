from bson.objectid import ObjectId

from fastapi import APIRouter, Depends

from .serializers import UserSerializer
from ..dependencies import database_connect

router = APIRouter()


@router.post("/user/")
async def user_create(user: UserSerializer, client=Depends(database_connect)):
    payload = user.model_dump()
    if "id" in payload:
        id = payload.pop("id")
        payload["_id"] = ObjectId(id)

    result = await client.auth.users.insert_one(payload)

    return {
        "message": "User created successfully",
        "user_id": str(result.inserted_id),
    }


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
