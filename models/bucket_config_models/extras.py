from typing import Literal

from pydantic import BaseModel


EXT_TYPE = Literal["png", "jpeg", "webp"]


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