from pydantic import BaseModel
from bson.objectid import ObjectId

class UserSerializer(BaseModel):
    id: str | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    active: bool = True
