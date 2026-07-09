from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL:str
    DATABASE_NAME:str
    ADMIN_USERNAME:str
    ADMIN_PASSWORD:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # pyright: ignore[reportCallIssue]