import os
from pathlib import Path
from typing import Self
from uuid import uuid4

from wand.image import Image
from models.bucket_config_models.extras import BucketImageSettings


class ProcessImage:
    def __init__(self, file_path: Path):
        self.image_path = file_path
        self.img = Image(filename=self.image_path)
        self.ext = str(self.image_path).split(".")[-1]
        self.new_path = Path("./processed_images")

    def resize_image(self, width: int, height: int) -> Self:
        self.img.resize(width=width, height=height)
        # self.img.transform(resize=f"{width}x")
        self.img.filter = "lanczos"
        return self

    def compress_image(self, quality: int = 82) -> Self:
        self.img.compression = "jpeg"  # compression type

        self.img.compression_quality = quality

        self.img.strip()  # removing metadata

        self.img.interlace_scheme = "plane"
        return self

    def change_file_extension(self, ext: str = "webp") -> Self:
        self.img.format = ext
        self.ext = ext
        return self

    def save(self) -> Path:

        if not os.path.exists(self.new_path):
            os.mkdir(self.new_path)

        filename = f"{uuid4()}.{self.ext}"
        output_path = self.new_path / filename
        self.img.save(filename=str(output_path))
        return output_path


def process_image(result: BucketImageSettings, path: Path) -> Path:
    current_process_image = ProcessImage(file_path=path)

    # image resize
    if result.resize:
        current_process_image.resize_image(
            height=result.resize.height,
            width=result.resize.width
        )

    # change file ext default: webp
    if result.change_file_ext.change_file_ext:
        current_process_image.change_file_extension(
            ext=result.change_file_ext.ext)

    # compress the image
    if result.compress_image:
        current_process_image.compress_image()

    # save the image
    processed_image_path = current_process_image.save()

    return processed_image_path
