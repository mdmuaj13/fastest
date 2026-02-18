from sqlalchemy import Column, Integer, String

from src.db.database import Base
from .mixins import TimestampMixin, SoftDeleteMixin

class UserModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)