from pydantic import BaseModel


class AdminLogin(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool = True
    message: str = "Login successfull"
