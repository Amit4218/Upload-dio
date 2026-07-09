import os
import shutil
import uuid

from fastapi import UploadFile

from src.utils.image_processer import process_image
from src.helpers.file_upload import validate_mime_type
from src.models.bucket import BucketConfig


def save_file_to_local(folder_path: str, files: list[UploadFile], bucket: BucketConfig) -> tuple[list[str], str]:
    """
    Save uploaded files to disk, optionally process images,
    and return a list of saved file paths.
    """

    file_urls: list[str] = []

    # Create the upload directory if it doesn't exist.
    folder_path = os.path.expanduser(f"~/Uplodio/{folder_path}")
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        save_path = os.path.join(folder_path, f"{uuid.uuid4()}-{file.filename}")

        # Default to the original file path.
        processed_image_path = save_path

        mime_type = str(file.content_type).split("/")[0]

        validate_mime_type(bucket, mime_type)

        # Save the uploaded file.
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process images if enabled.
        if bucket.image_settings.modify_image and mime_type == "image":
            processed_image_path = process_image(
                result=bucket.image_settings,
                path=save_path,
                folder_path=folder_path,
            )

        file_urls.append(processed_image_path)

    return file_urls, folder_path