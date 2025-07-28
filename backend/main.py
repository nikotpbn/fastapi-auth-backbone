from fastapi import Depends, FastAPI

from .dependencies import database_connect
from .auth import auth_router as auth

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/")
async def home():
    return {"message": "Hello, World!"}
