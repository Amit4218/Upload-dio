import jwt
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import  OAuth2PasswordBearer
from pwdlib import PasswordHash

from src.config.db import get_collection
from src.config.settings import settings
from src.models.admin import Admin


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
password_hash = PasswordHash.recommended()


async def create_default_admin() -> None:
    
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


async def is_admin(token: str = Depends(oauth2_scheme)) -> bool:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return True
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )