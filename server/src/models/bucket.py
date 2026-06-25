from pydantic import BaseModel
from typing import Literal, List


EXT_TYPE = Literal["png", "jpeg", "webp"]
BUCKET_HOST  = Literal["server"]


class Resize(BaseModel):
    resize_image: bool = False
    height: int
    width: int

class ChangeFileExtention(BaseModel):
    change_file_ext: bool = False
    ext: EXT_TYPE = "webp"


class BucketImageSettings(BaseModel):
    modify_image:bool
    resize: Resize
    compress_image:bool = False
    change_file_ext: ChangeFileExtention


class BucketConfig(BaseModel):
    bucket_host: BUCKET_HOST = "server"
    bucket_name: str
    allowed_origin: str
    maxfiles: int = 1
    save_folder_path:str
    public_access_id:str
    include_videos: bool = False
    include_files: bool = False
    include_audio: bool = False
    callback_url: str | None = None
    image_settings: BucketImageSettings
    images:List[str] = []