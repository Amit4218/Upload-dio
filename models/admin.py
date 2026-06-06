from pydantic import BaseModel

class Admin(BaseModel):
    username:str
    password: str
    super_admin_pass: str | None = None
    is_active: bool = False