from __future__ import annotations

from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class ReservationDisableBase(BaseModel):
    room_id: int
    facility_id: int

    reason: Optional[str] = None

    disable_date: date
    disable_start_at: datetime
    disable_end_at: datetime


class ReservationDisableCreate(ReservationDisableBase):
    pass


class ReservationDisableCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    disable_id: int
    message: str = "created"


class ReservationDisableDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    disable_id: int
    room_id: int
    facility_id: int
    reason: Optional[str]

    disable_date: date
    disable_start_at: datetime
    disable_end_at: datetime


class ReservationDisableListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    disable_id: int
    room_id: int
    facility_id: int
    reason: Optional[str]
    disable_start_at: datetime
    disable_end_at: datetime


class ReservationDisableListResponse(BaseModel):
    items: List[ReservationDisableListItemResponse]
    total_count: int