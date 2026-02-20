from __future__ import annotations

from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from schemas.student import StudentDetail
from schemas.study_room import StudyRoomDetail
from schemas.facility import FacilityDetailResponse


class ReservationBase(BaseModel):
    room_id: int
    facility_id: int

    reservation_date: date
    reservation_start_date: datetime
    reservation_end_date: datetime

    reservation_count: Optional[int] = None
    use_tf: bool = True


class ReservationCreate(ReservationBase):
    pass


class ReservationCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: int
    message: str = "created"


class ReservationDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_item: Optional[StudentDetail] = None
    room_item: Optional[StudyRoomDetail] = None
    facility_item: Optional[FacilityDetailResponse] = None

    reservation_id: int

    student_id: int
    room_id: int
    facility_id: int

    reservation_status: str
    reservation_date: date
    reservation_start_date: datetime
    reservation_end_date: datetime

    reservation_count: Optional[int]
    use_tf: bool

    reg_date: date
    up_date: date
    del_date: date
    cancel_date: Optional[date]


class ReservationListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: int

    student_id: int
    room_id: int
    facility_id: int

    student_item: Optional[StudentDetail] = None
    room_item: Optional[StudyRoomDetail] = None
    facility_item: Optional[FacilityDetailResponse] = None

    reservation_status: str
    reservation_date: date
    reservation_start_date: datetime
    reservation_end_date: datetime

    reservation_count: Optional[int]
    use_tf: bool


class ReservationListResponse(BaseModel):
    items: List[ReservationListItemResponse]
    total_count: int