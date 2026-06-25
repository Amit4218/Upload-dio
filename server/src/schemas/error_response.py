from pydantic import BaseModel


class FileUploadCallBackError(BaseModel):
    message:str
    urls:list[str]