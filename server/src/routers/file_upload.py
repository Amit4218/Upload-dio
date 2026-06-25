import os
import shutil
import uuid
import requests

from fastapi import HTTPException, UploadFile, File, Request, status
from fastapi.routing import APIRouter

from src.config.db import get_collection
from src.models.bucket import BucketConfig
from src.utils.image_processer import process_image
from src.schemas.success_response import FileUploadSuccess
from src.schemas.error_response import FileUploadCallBackError

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

    # get data for the bucket config
    result = await bucket_collection.find_one({"public_access_id": bucket_id})

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no bucket found!"
        )
        
    bucket = BucketConfig(**result)
    
    
    # the max no of files that can be uploaded at once
    if len(files) > bucket.maxfiles:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"files count exceeds the max limit for file upload at once: ({bucket.maxfiles})"
        )
        
    allowed_origin = bucket.allowed_origin
    
    # check if the origin is allowed
    if allowed_origin != "*" and req.headers.get("origin") != allowed_origin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="origin not allowed to upload to this bucket"
        )
    
    # save the images in the given path
    folder_path = result.get("save_folder_path")
    
        
    # create the directory
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        
    file_urls = []

    for file in files:
        save_path = f"{folder_path}/{uuid.uuid4()}-{file.filename}"
        processed_image_path = save_path
        
        meme_type = str(file.content_type).split("/")[0]
        
        
        if meme_type == "video" and not bucket.include_videos:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="videos uploads are not supported"
            )
            
            
        if meme_type == "audio" and not bucket.include_audio:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="audio uploads are not supported"
            )
            
            
        if meme_type == "application" and not bucket.include_files:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="files uploads are not supported"
            )
            
        
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        
        # process the images only
        if bucket.image_settings.modify_image and meme_type == "image":
            processed_image_path = process_image(
                result=bucket.image_settings,
                path=save_path,
                folder_path=folder_path
            )
        
        # determine the image file path
        file_urls.append(processed_image_path)
    
    await bucket_collection.update_one(
        {"public_access_id": bucket_id},
            {
                "$push": {
                    "images": {
                        "$each": [img for img in file_urls]
                    }
                }   
            }
    )
    
    if bucket.callback_url:
        res = requests.post(bucket.callback_url, json={"image_urls":file_urls})

        if res.status_code != 200:
            return FileUploadCallBackError(message="error during callback", urls=file_urls)
        
    
    return FileUploadSuccess(message="file uploaded successfully", urls=file_urls)