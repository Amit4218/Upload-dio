from sqlalchemy import Column, Integer, String

from config.db import Base, Session


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    @classmethod
    def exists(cls, db: Session) -> bool:
        admin_count = db.query(cls).count()
        return admin_count > 0
