Project
A basic authentication system with FastAPI

Nuances

MongoDB ObjectId is not supported by Pydantic. Thus, it has to be cast into string for response.
(Just as it has ti be cast from a string into a ObjectID when inserting.)
```
@router.get("/user/{user_id}")
async def user_detail(user_id: str, client=Depends(database_connect)):
    response = await client.auth.users.find_one({"_id": ObjectId(user_id)})

    if response:
        response["_id"] = str(response["_id"])
        return response

    return {"message": "User not found"}
```