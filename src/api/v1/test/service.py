from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from typing import List, Optional

from src.db.database import Base, get_db
from src.models.test import TestModel
from .schema import TestCreate, TestUpdate


# Service functions
def create_test(db, data: TestCreate) -> TestModel:
    db_test = TestModel(**data.model_dump())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


def get_tests(db, page: int = 1, limit: int = 10) -> List[TestModel]:
    skip = (page - 1) * limit
    return db.query(TestModel).offset(skip).limit(limit).all()


def get_test(db, test_id: int) -> Optional[TestModel]:
    return db.query(TestModel).filter(TestModel.id == test_id).first()


def update_test(db, test_id: int, data: TestUpdate) -> Optional[TestModel]:
    db_test = db.query(TestModel).filter(TestModel.id == test_id).first()
    if db_test:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_test, key, value)
        db.commit()
        db.refresh(db_test)
    return db_test


def delete_test(db, test_id: int) -> bool:
    db_test = db.query(TestModel).filter(TestModel.id == test_id).first()
    if db_test:
        db.delete(db_test)
        db.commit()
        return True
    return False
