from pydantic import BaseModel
from typing import Literal, Optional


EXT_TYPE = Literal["png", "jpeg", "webp"]


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


class BucketConfigSchema(BaseModel):
    bucket_name: str
    allowed_origin: str
    maxfiles: int = 1
    save_folder_path:str
    include_videos: bool = False
    include_files: bool = False
    include_audio: bool = False
    callback_url: str | None = None
    image_settings: Optional[BucketImageSettings] = None