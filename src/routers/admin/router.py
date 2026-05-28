from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, Form, Request, HTTPException, status
from sqlalchemy import select

from config.db import get_db, Session
from models.admin import Admin
from src.routers.admin.schemas.auth import AdminLogin, LoginResponse

admin_router = APIRouter(prefix="/api/auth", tags=["auth"])


@admin_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_admin(
    req: Request,
    data: Annotated[AdminLogin, Form()],
    db: Session = Depends(get_db)
) -> LoginResponse:

    admin = db.execute(
        select(Admin).where(
            Admin.username == data.username
        )
    ).scalar_one_or_none()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    is_pass_correct = Admin.verify_password(
        data.password,
        admin.password
    )

    if not is_pass_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
        
    # set session for the admin
