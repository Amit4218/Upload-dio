from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from models.bucket_config import BucketConfig
from src.routers.dashboard.schemas.dashnoard import CreateNewBucket, SuccessBucketCreation
from config.db import get_db

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@dashboard_router.get("/")
def get_metadata(db: Session = Depends(get_db)):
    pass


@dashboard_router.post("/create-bucket", status_code=status.HTTP_200_OK)
async def create_new_bucket(
    data: CreateNewBucket,
    db: Session = Depends(get_db)
    
) -> SuccessBucketCreation:
    
    new_bucket = BucketConfig(**data.model_dump())
    new_bucket.generate_public_access_id()
    
    public_id = new_bucket.public_access_id
    
    db.add(new_bucket)
    db.commit()
    db.refresh(new_bucket)

    return SuccessBucketCreation(public_access_id=public_id)
