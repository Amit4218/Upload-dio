from sqlalchemy import Column, Integer, String
from config.db import Base, Session
from src.utils.settings import settings
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    @classmethod
    def exists(cls, db: Session) -> bool:
        admin_count = db.query(cls).count()
        return admin_count > 0

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_pass: str, hashed_password: str) -> bool:
        return pwd_context.verify(
            plain_pass,
            hashed_password
        )


def create_admin(db: Session) -> str:

    already_exist = Admin.exists(db=db)

    if already_exist:
        return "Admin already exists"

    if not settings.ADMIN_USERNAME or not settings.ADMIN_PASSWORD:
        raise Exception(
            "No admin username or password found in .env"
        )

    hashed_password = Admin.hash_password(settings.ADMIN_PASSWORD)

    admin = Admin(
        username=settings.ADMIN_USERNAME,
        password=hashed_password
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return "Admin created successfully"
