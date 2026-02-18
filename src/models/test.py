from sqlalchemy import Column, Integer, String
from src.db.database import Base
from .mixins import TimestampMixin, SoftDeleteMixin

class TestModel(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
