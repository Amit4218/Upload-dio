from fastapi import HTTPException, UploadFile, File
from fastapi.routing import APIRouter
from schemas.image import ImageUploadSuccess
import os
import shutil

image_upload_router = APIRouter(prefix="/api/upload", tags=["image_upload"])


@image_upload_router.post("/{bucket_id}", response_model=ImageUploadSuccess)
def upload_image_to_bucket(bucket_id: str, file: UploadFile = File(...)):

    if not file:
        raise HTTPException(status_code=404, detail="file not found")

    try:
        os.makedirs("uploads", exist_ok=True)

        save_path = f"uploads/{file.filename}"

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # process the images

        return ImageUploadSuccess(
            success=True,
            message="File uploaded successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
