from fastapi import HTTPException, status

from src.models.bucket import BucketConfig

def validate_mime_type(bucket: BucketConfig,  mime_type:str) -> None:
    """vadlidates if the file is allowed in in the endpoint, by verfying the file mimetype"""
    
    if mime_type == "video" and not bucket.include_videos:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="video file uploads are not set to allowed"
        )
        
        
    if mime_type == "audio" and not bucket.include_audio:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="audio file uploads are not set to allowed"
        )
        
        
    if mime_type == "application" and not bucket.include_files:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="files uploads are not set to allowed"
        )