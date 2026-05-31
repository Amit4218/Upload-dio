import secrets

from fastapi import Depends, status
from fastapi.routing import APIRouter

from models.bucket_config import BucketConfig
from src.routers.dashboard.schemas.dashnoard import SuccessBucketCreation,CreateBucketConfig
from config.db import get_collection
from src.utils.get_admin import is_admin

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@dashboard_router.get("/")
def get_metadata(
    _ = Depends(is_admin)
):
    pass


@dashboard_router.post("/create-bucket", status_code=status.HTTP_201_CREATED)
async def create_new_bucket(
    data: CreateBucketConfig,
    _=Depends(is_admin)
) -> SuccessBucketCreation:

    bucket_collection = get_collection("bucket_config")

    payload = data.model_dump()
    
    # generate an public access id for the client
    payload["public_access_id"] = secrets.token_urlsafe(12)

    new_bucket = BucketConfig(**payload)

    await bucket_collection.insert_one(
        new_bucket.model_dump()
    )

    return SuccessBucketCreation(
        public_access_id=new_bucket.public_access_id
    )
