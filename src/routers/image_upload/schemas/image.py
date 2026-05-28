from pydantic import BaseModel


class ImageUploadSuccess(BaseModel):
    success: bool = True
