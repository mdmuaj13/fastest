from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TestBase(BaseModel):
    name: str
    description: Optional[str] = None


class TestCreate(TestBase):
    pass


class TestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TestResponse(TestBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
