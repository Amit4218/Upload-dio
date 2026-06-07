# This model belongs to the FastAPI  Application settings, 
# Please don't edit the model as it may cause issues with the application configuration.

from pydantic import BaseModel
from typing import Dict, Any
from config.db import get_collection

class ApplicationSettings(BaseModel):
    title: str = "Upload-dio API"
    summary: str = "A single api-gateway to upload your files, images and videos to different cloud bucket, with dashboard monitoring."
    description: str = "(Up-load-di-o) aims to provide users with a single api-gateway for handling file uploads like, images, videos, pdf etc. with currently, it only supports image related operation with available features like, image resize, compression and extention changer."
    version: str = "1.0.0"
    contact: Dict[str, str] = {
        "name": "Amit Bhagat",
        "email": "amitbhagat621+uploadio@gmail.com",
    }
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str = "/openapi.json"
    swagger_ui_parameters: Dict[str, Any] = {
        "persistAuthorization": True
    }
    
class ExtraSettings(BaseModel):
    isRestartRequired: bool = False


async def create_default_settings() -> None:
    settings_collection = get_collection("app_settings")
    existing_settings = await settings_collection.count_documents({})
    
    if existing_settings == 0:
        await settings_collection.insert_one({
            **ApplicationSettings().model_dump(),
            **ExtraSettings().model_dump()
        })