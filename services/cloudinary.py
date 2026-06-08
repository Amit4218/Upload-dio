from pathlib import Path

import cloudinary
from cloudinary.uploader import upload


class CloudinaryService:
    
    
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True
        )

    def upload_image(self, file_path: Path, public_id: str = None) -> str:
        try:
            response = upload(file_path, public_id=public_id)
            return response['secure_url']
            
        except Exception as e:
            raise Exception(f"Error uploading image: {e}")
