from pydantic import BaseModel

class CloudflareConfig(BaseModel):
    access_id: str
    access_secret: str
    bucket_url: str
