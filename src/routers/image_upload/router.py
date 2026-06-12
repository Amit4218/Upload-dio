import os
import shutil

from fastapi import HTTPException, UploadFile, File, Request
from fastapi.routing import APIRouter

from config.db import get_collection
from models.bucket_config import BucketConfig, Images
from src.routers.image_upload.schemas.image import ImageUploadSuccess
from src.utils.process_image import process_image
from services import upload_image_to_cloudinary

image_upload_router = APIRouter(prefix="/api/upload", tags=["image_upload"])


@image_upload_router.post("/{bucket_id}")
async def upload_image_to_bucket(
        req:Request,
        bucket_id: str,
        files: list[UploadFile] = File(...),
) -> ImageUploadSuccess:

    if not files:
        raise HTTPException(status_code=404, detail="file not found")

    bucket_collection = get_collection("bucket_config")

    # get data for the bucket config
    result = await bucket_collection.find_one({"public_access_id": bucket_id})

    if not result:
        raise HTTPException(
            status_code=400, detail="no bucket found!")
        
    allowed_origin = result.get("allowed_origin")
    
    if allowed_origin != "*" and req.headers.get("origin") not in allowed_origin:
        raise HTTPException(
            status_code=403, detail="origin not allowed to upload to this bucket")

    bucket = BucketConfig(**result)

    try:
        os.makedirs("uploads", exist_ok=True)
        
        images: list[Images] = []

        for file in files:

            save_path = f"uploads/{file.filename}"

            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # process the images
            if bucket.image_settings:
                processed_image_path = process_image(
                    result=bucket.image_settings,
                    path=save_path
                )
                
            # determine the image file path
            file_path = processed_image_path if bucket.image_settings else save_path

            # upload the image to the cloud bucket
            match bucket.bucket_provider:

                case 'CLOUDINARY':
                    
                    url = upload_image_to_cloudinary(
                        cloud_name=bucket.provider_config.cloud_name,
                        api_key=bucket.provider_config.api_key,
                        api_secret=bucket.provider_config.api_secret,
                        file_path=file_path,
                        public_id=file.filename
                    )
                    
                    images.append(Images(
                        url=url,
                        filename=file.filename
                    ))
                                    
                case 'IMAGEKIT':
                    pass

                case 'AWS':
                    pass

                case 'CLOUDFLARE':
                    pass

                case _:
                    pass
        
        # update the bucket collection with the new image urls
        await bucket_collection.update_one(
            {"public_access_id": bucket_id},
                {
                    "$push": {
                        "images": {
                            "$each": [img.model_dump() for img in images]
                        }
                    }   
                }
        )
        
        return ImageUploadSuccess

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        os.remove(path=save_path)
        os.remove(path=processed_image_path)
