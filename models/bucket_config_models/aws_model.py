from pydantic import BaseModel


class AWSConfig(BaseModel):
    access_id: str
    access_secret: str
    bucket_url: str