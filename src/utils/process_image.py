from wand.image import Image
from pathlib import Path
from typing import Self
from uuid import uuid4


class ProcessImage:
    def __init__(self, file_path: Path):
        self.image_path = file_path
        self.img = Image(filename=self.image_path)
        self.ext = str(self.image_path).split(".")[-1]
        self.new_path = Path("./static")

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

    def save(self) -> Self:
        filename = f"{uuid4()}.{self.ext}"
        output_path = self.new_path / filename
        self.img.save(filename=str(output_path))
        return self
