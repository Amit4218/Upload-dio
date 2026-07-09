import secrets

from fastapi import Depends
from fastapi.routing import APIRouter

from src.config.db import get_collection
from src.schemas.bucket import BucketConfigSchema
from src.models.bucket import BucketConfig
from src.utils.admin import is_admin
from src.schemas.success_response import BucketCreationSuccess

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@dashboard_router.post("/create_bucket", response_model=BucketCreationSuccess)
async def create_bucket_config(data:BucketConfigSchema, _ = Depends(is_admin)):
    
    bucket_collection = get_collection("bucket_config")
    
    payload = data.model_dump()
    
    # generate an public access id for the client
    payload["public_access_id"] = secrets.token_urlsafe(12)

    new_bucket = BucketConfig(**payload, providers=None)

    await bucket_collection.insert_one(
        new_bucket.model_dump()
    )

    return BucketCreationSuccess(public_id=new_bucket.public_access_id)