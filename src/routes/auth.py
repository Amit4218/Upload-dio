from fastapi.routing import APIRouter
from models.admin import Admin
from fastapi import Depends, Form, Request, HTTPException
from config.db import get_db, Session
from sqlalchemy import select
from typing import Annotated
from schemas.auth import AdminLogin, LoginResponse

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])


@auth_router.post("/login", response_model=LoginResponse)
def login_admin(
    req: Request,
    data: Annotated[AdminLogin, Form()],
    db: Session = Depends(get_db)
):

    admin = db.execute(
        select(Admin).where(
            Admin.username == data.username
        )
    ).scalar_one_or_none()

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    is_pass_correct = Admin.verify_password(
        data.password,
        admin.password
    )

    if not is_pass_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Set Session
    req.session["id"] = admin.id

    return LoginResponse(status_code=200, success=True)
