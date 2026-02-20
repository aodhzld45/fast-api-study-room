# /schemas/facility.py

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict

class FacilityBase(BaseModel):
    facility_name: str = Field(..., max_length=100)
    facility_address: str = Field(..., max_length=50)
    facility_desc: str = Field(..., max_length=50)
    use_tf: bool = True


class FacilityCreate(FacilityBase):
    """POST /facilities 요청 바디"""
    pass


class FacilityCreateResponse(BaseModel):
    """생성 결과(최소)"""
    model_config = ConfigDict(from_attributes=True)

    facility_id: int
    message: str = "created"

class FacilityDetailResponse(BaseModel):
    """GET /facilities/{id} 응답"""
    model_config = ConfigDict(from_attributes=True)

    facility_id: int
    facility_name: str
    facility_address: str
    facility_desc: str
    use_tf: bool

    reg_date: datetime
    up_date: datetime
    del_date: datetime


class FacilityListItemResponse(BaseModel):
    """목록 아이템(가볍게)"""
    model_config = ConfigDict(from_attributes=True)

    facility_id: int
    facility_name: str
    facility_address: str
    use_tf: bool


class FacilityListResponse(BaseModel):
    """GET /facilities 응답(페이징 없음)"""
    items: List[FacilityListItemResponse]
    total_count: int