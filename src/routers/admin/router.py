from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
import jwt

from config.db import get_collection
from models.admin import Admin
from src.utils.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
password_hash = PasswordHash.recommended()

admin_router = APIRouter(prefix="/api/auth", tags=["auth"])


async def create_admin() -> None:
    
    admin_collection = get_collection("admin")
    
    already_exist = await admin_collection.count_documents({})

    if already_exist > 0:
        return

    if not settings.ADMIN_USERNAME or not settings.ADMIN_PASSWORD:
        raise Exception("No admin username or password found in .env")

    hashed_password = password_hash.hash(settings.ADMIN_PASSWORD)

    await admin_collection.insert_one(
        Admin(
            username=settings.ADMIN_USERNAME,
            password=hashed_password
        ).model_dump()
    )


@admin_router.post("/login")
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

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }