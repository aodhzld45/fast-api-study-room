from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict
from schemas.student import StudentDetail


class ReviewBase(BaseModel):
    room_id: int
    rating: int = Field(..., ge=1, le=5)  # 1~5
    comment: str = Field(..., max_length=255)


class ReviewCreate(ReviewBase):
    pass


class ReviewCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_id: int
    message: str = "created"


class ReviewDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_id: int
    room_id: int
    student_id: int

    rating: int
    comment: str

    student_item: StudentDetail

    reg_date: Optional[datetime] = None

class ReviewListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    review_id: int
    room_id: int
    student_id: int

    rating: int
    comment: str

    reg_date: Optional[datetime] = None

class ReviewListResponse(BaseModel):
    items: List[ReviewListItemResponse]
    total_count: int
