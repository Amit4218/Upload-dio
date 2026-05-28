from fastapi import HTTPException, UploadFile, File, Depends
from fastapi.routing import APIRouter
from config.db import get_db, Session
from models.bucket_config import BucketConfig
from src.routers.image_upload.schemas.image import ImageUploadSuccess
from src.utils.process_image import ProcessImage
import os
import shutil

image_upload_router = APIRouter(prefix="/api/upload", tags=["image_upload"])


@image_upload_router.post("/test")
async def upload_images(images: list[UploadFile] = File(...)):
    print(len(images))
    return {"uploaded": True}


@image_upload_router.post("/{bucket_id}")
async def upload_image_to_bucket(
        bucket_id: str,
        h: int = None,
        w: int = None,
        ext: str = "webp",
        file: UploadFile = File(...),
        db: Session = Depends(get_db)

) -> ImageUploadSuccess:

    if not file:
        raise HTTPException(status_code=404, detail="file not found")

    try:
        os.makedirs("uploads", exist_ok=True)

        save_path = f"uploads/{file.filename}"

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # get data for the bucket config
        result = db.query(BucketConfig).filter_by(
            public_access_id=bucket_id).first()

        if not result:
            raise HTTPException(
                status_code=400, detail="no bucket found!")

        # process the images
        current_process_image = ProcessImage(file_path=save_path)

        # image resize
        if w and h:
            current_process_image.resize_image(height=h, width=w)

        # change file ext default: webp
        current_process_image.change_file_extension(ext=ext)

        # compress the image
        current_process_image.compress_image()

        # save the image
        current_process_image.save()

        # upload the image to the cloud bucket

        return ImageUploadSuccess(
            success=True,
            message="File uploaded successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        os.remove(path=save_path)
