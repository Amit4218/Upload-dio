from pydantic import BaseModel

class Admin(BaseModel):
    username:str
    password: str
    email: str | None = None
    super_admin_pass: str | None = None
    is_active: bool = False