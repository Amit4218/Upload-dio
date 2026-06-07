from pydantic import BaseModel

class CloudinaryConfig(BaseModel):
    cloud_name: str
    api_key: str
    api_secret: str