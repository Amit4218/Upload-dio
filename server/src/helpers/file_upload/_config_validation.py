from fastapi import UploadFile, HTTPException, status, Request

from src.models.bucket import BucketConfig


def validate_configs(bucket:BucketConfig, files: list[UploadFile], req:Request) -> None:
    """validates configuration requirements like maxfiles, allowed origin"""
    
    # the max no of files that can be uploaded at once
    if len(files) > bucket.maxfiles:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"files count exceeds the max limit for file upload at once: Limit ({bucket.maxfiles})"
        )
        
    allowed_origin = bucket.allowed_origin
    
    # check if the origin is allowed
    if allowed_origin != "*" and req.headers.get("origin") != allowed_origin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="origin not allowed to upload to this bucket"
        )