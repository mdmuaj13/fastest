from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.db.database import get_db
from src.utils.responser import ApiResponse
from .schema import TestCreate, TestUpdate, TestResponse
from .service import create_test, get_tests, get_test, update_test, delete_test

router = APIRouter(prefix="/test", tags=["Test"])


@router.post("/", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
def create(data: TestCreate, db: Session = Depends(get_db)):
    """Create a new test record"""
    test = create_test(db, data)
    return ApiResponse(data=test, message="Test created successfully")


@router.get("/", response_model=List[TestResponse])
def list_all(page: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all test records"""
    data = get_tests(db, page, limit)
    return ApiResponse(data=data, message="Tests retrieved successfully")


@router.get("/{test_id}", response_model=TestResponse)
def get_one(test_id: int, db: Session = Depends(get_db)):
    """Get a specific test record by ID"""
    db_test = get_test(db, test_id)
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return ApiResponse(data=db_test, message="Test retrieved successfully")


@router.put("/{test_id}", response_model=TestResponse)
def update(test_id: int, data: TestUpdate, db: Session = Depends(get_db)):
    """Update a test record"""
    db_test = update_test(db, test_id, data)
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return ApiResponse(data=db_test, message="Test updated successfully")


@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(test_id: int, db: Session = Depends(get_db)):
    """Delete a test record"""
    if not delete_test(db, test_id):
        raise HTTPException(status_code=404, detail="Test not found")
    return ApiResponse(data=None, message="Test deleted successfully")
