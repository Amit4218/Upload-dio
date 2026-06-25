from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash

from src.config.db import get_collection
from src.config.settings import settings
from src.schemas.success_response import LoginSuccess


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
password_hash = PasswordHash.recommended()

admin_router = APIRouter(prefix="/api/auth", tags=["auth"])

@admin_router.post("/login", response_model=LoginSuccess)
async def login_admin(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    
    admin_collection = get_collection("admin")

    admin = await admin_collection.find_one({"username":data.username})

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    is_pass_correct = password_hash.verify(
        data.password,
        admin["password"]
    )

    if not is_pass_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    access_token = jwt.encode(
        {
            "sub": str(admin["_id"]),
            "exp": expire
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return  LoginSuccess(access_token=access_token, token_type="bearer")