import jwt
import certifi
from datetime import datetime
from jwt.exceptions import InvalidTokenError

from typing import Annotated
from datetime import timedelta

from pymongo import AsyncMongoClient

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from .utils import get_secret
from .auth.serializers import UserSerializer

MONGO_URI = get_secret("MONGO_URI", "")
SECRET_KEY = get_secret("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


# Send a ping to confirm a successful connection
async def database_connect() -> None:
    try:
        client = AsyncMongoClient(MONGO_URI, tlsCAFile=certifi.where())
        await client.aconnect()
        await client.admin.command("ping")
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)


async def get_user(client: AsyncMongoClient, email: str) -> UserSerializer | None:
    user = await client.auth.users.find_one(
        {"email": email}, projection=["email", "password"]
    )
    if user:
        user["_id"] = str(user["_id"])
    return user


async def get_current_user(
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
    client: AsyncMongoClient = Depends(database_connect),
) -> UserSerializer | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            return credentials_exception

    except InvalidTokenError:
        return None

    user = await get_user(client, email)
    if user is None:
        raise credentials_exception

    return user


async def authenticate_user(client: AsyncMongoClient, username: str, password: str):
    """
    Username is email, but as for OAuth2 specs it is called username.
    """
    user = await get_user(client, username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + timedelta(minutes=30)
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
