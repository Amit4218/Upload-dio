from pydantic import BaseModel
from typing import Literal, List, Optional, Union

from models.bucket_config_models.cloudinary_models import CloudinaryConfig
from models.bucket_config_models.imagekit_model import ImageKitConfig
from models.bucket_config_models.cloudflare_model import CloudflareConfig
from models.bucket_config_models.aws_model import AWSConfig
from models.bucket_config_models.extras import BucketImageSettings


BucketProviderType = Literal["AWS", "CLOUDFLARE", "CLOUDINARY","IMAGEKIT"]


class Images(BaseModel):
    filename:str
    url:str

class BucketConfig(BaseModel):
    bucket_provider: BucketProviderType
    bucket_name: str
    provider_config: Union[AWSConfig, CloudflareConfig, CloudinaryConfig, ImageKitConfig]
    allowed_origin: str
    public_access_id:str
    image_settings: BucketImageSettings
    images:Optional[List[Images]] = None