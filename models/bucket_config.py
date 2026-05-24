from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
from typing import Self, Literal
from datetime import datetime
import secrets


BucketType = Literal["AWS", "CLOUDFLARE"]


class BucketConfig(Base):
    __tablename__ = "bucket_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False, default="CLOUDFLARE")
    bucket_name = Column(String, nullable=False)
    access_id = Column(String, nullable=False)
    access_secret = Column(String, nullable=False)
    allowed_origin = Column(String, nullable=False)
    bucket_url = Column(String, nullable=False)
    public_access_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    images = relationship("Images", back_populates="bucket",
                          cascade="all, delete-orphan")

    def generate_public_access_id(self) -> Self:
        self.public_access_id = secrets.token_urlsafe(12)
        return self


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    url = Column(String, nullable=False)
    bucket_id = Column(Integer, ForeignKey("bucket_config.id"), nullable=False)
    bucket = relationship("BucketConfig", back_populates="images")
    created_at = Column(DateTime, default=datetime.utcnow)
