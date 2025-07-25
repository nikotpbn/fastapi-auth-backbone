from fastapi import Depends, FastAPI

from .routers import auth

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
async def home():
    return {"message": "Hello, World!"}