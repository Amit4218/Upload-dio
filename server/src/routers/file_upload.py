import shutil
import requests
from fastapi import HTTPException, UploadFile, File, Request, status
from fastapi.routing import APIRouter

from src.config.db import get_collection
from src.models.bucket import BucketConfig
from src.schemas.success_response import FileUploadSuccess
from src.schemas.error_response import FileUploadCallBackError
from src.services.aws_client import AwsS3Uploader
from src.helpers.file_upload import validate_configs, save_file_to_local

file_upload_router = APIRouter(prefix="/api/upload", tags=["image_upload"])


@file_upload_router.post("/{bucket_id}", response_model=FileUploadSuccess | FileUploadCallBackError)
async def upload_image(
        req:Request,
        bucket_id: str,
        files: list[UploadFile] = File(...)
):
    
    if not files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="files not found"
        )
    
    bucket_collection = get_collection("bucket_config")

    # get the bucket config
    result = await bucket_collection.find_one({"public_access_id": bucket_id})

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no bucket found!"
        )
        
    bucket = BucketConfig(**result)
    
    validate_configs(bucket, files, req)
    
    file_paths, files_folder = save_file_to_local(bucket.save_folder_path, files, bucket)
    
    # upload the files to the s3 bucket
    if bucket.bucket_host == "s3":
        
        if not bucket.providers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no provider found!"
            )
        
        file_paths = await AwsS3Uploader.client(bucket.providers).upload_files_to_bucket(files=file_paths)
        
        # remove the local folder
        shutil.rmtree(files_folder)
    
    
    # send the image urls to the callback endpoint
    if bucket.callback_url:
        res = requests.post(bucket.callback_url, json={"image_urls":file_paths})

        if res.status_code != 200:
            
            # delete the uploaded files if an error occur
            if bucket.providers:
                await AwsS3Uploader.client(bucket.providers).delete_file_from_bucket(file_paths)
                
            return FileUploadCallBackError(message="error during callback", urls=[])


    await bucket_collection.update_one(
        {"public_access_id": bucket_id},
            {
                "$push": {
                    "images": {
                        "$each": [img for img in file_paths]
                    }
                }   
            }
    )
    
  
    return FileUploadSuccess(message="file uploaded successfully", urls=file_paths)