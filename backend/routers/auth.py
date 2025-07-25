from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.get("/token", tags=["auth"])
async def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
