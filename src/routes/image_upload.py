from fastapi.routing import APIRouter


image_upload_router = APIRouter(prefix="/api/upload", tags=["image_upload"])


@image_upload_router.post("/{bucket_id}")
def upload_image_to_bucket(bucket_id: str):
    print(bucket_id)
    return {"status": "ok"}
