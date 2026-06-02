from pydantic import BaseModel
from typing import  Literal, Union

BucketProviderType = Literal["AWS", "CLOUDFLARE", "CLOUDINARY","IMAGEKIT"]
EXT_TYPE = Literal["png", "jpeg", "webp"]


class CloudinaryConfig(BaseModel):
    cloud_name: str
    api_key: str
    api_secret: str
    

class ImageKitConfig(BaseModel):
    public_key: str
    private_key: str
    url_endpoint: str
    
class AWSConfig(BaseModel):
    access_id: str
    access_secret: str
    bucket_url: str

class CloudflareConfig(BaseModel):
    access_id: str
    access_secret: str
    bucket_url: str


class Resize(BaseModel):
    resize_image: bool = False
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
    provider_config: Union[AWSConfig, CloudflareConfig, CloudinaryConfig, ImageKitConfig]
    allowed_origin: str
    image_settings: BucketImageSettings


class SuccessBucketCreation(BaseModel):
    success: bool = True
    public_access_id: str
