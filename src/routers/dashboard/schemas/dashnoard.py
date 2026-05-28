from pydantic import BaseModel
from typing import Literal

BucketType = Literal["AWS", "CLOUDFLARE", "CLOUDINARY","IMAGEKIT"]

class CreateNewBucket(BaseModel):
    type: BucketType
    bucket_name: str
    access_id: str
    access_secret: str
    allowed_origin: str
    bucket_url: str


class SuccessBucketCreation(BaseModel):
    success: bool = True
    public_access_id: str
