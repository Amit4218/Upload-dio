from pydantic import BaseModel


class FileUploadSuccess(BaseModel):
    message:str
    urls:list[str]
    
    
class BucketCreationSuccess(BaseModel):
    public_id:str
    
class LoginSuccess(BaseModel):
    access_token:str
    token_type:str