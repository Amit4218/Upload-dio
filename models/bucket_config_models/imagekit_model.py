from pydantic import BaseModel


class ImageKitConfig(BaseModel):
    public_key: str
    private_key: str
    url_endpoint: str