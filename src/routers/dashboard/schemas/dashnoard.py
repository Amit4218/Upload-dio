from pydantic import BaseModel
from typing import  Literal

BucketProviderType = Literal["AWS", "CLOUDFLARE", "CLOUDINARY","IMAGEKIT"]
EXT_TYPE = Literal["png", "jpeg", "webp"]


class Resize(BaseModel):
    height: int
    width: int

class ChangeFileExtention(BaseModel):
    change_file_ext: bool = False
    ext: EXT_TYPE = "webp"

class BucketImageSettings(BaseModel):
    resize: Resize
    compress_image:bool
    change_file_ext: ChangeFileExtention

class CreateBucketConfig(BaseModel):
    bucket_provider: BucketProviderType
    bucket_name: str
    access_id: str
    access_secret: str
    allowed_origin: str
    bucket_url: str
    image_settings: BucketImageSettings


class SuccessBucketCreation(BaseModel):
    success: bool = True
    public_access_id: str
