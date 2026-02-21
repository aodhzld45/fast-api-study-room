from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict
from schemas.facility import FacilityDetailResponse
from schemas.review import ReviewListItemResponse

class StudyRoomBase(BaseModel):
    facility_id: int
    room_name: str = Field(..., max_length=100)
    room_floor: str = Field(..., max_length=50)
    room_image: str = Field(..., max_length=50)
    room_capacity: int
    room_equipment: str
    use_tf: bool = True
    
class StudyRoomCreate(StudyRoomBase):
    pass

class StudyRoomCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    room_id: int
    message: str = "created"

class StudyRoomDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    facility_item: FacilityDetailResponse
    review_items: List[ReviewListItemResponse] = []    
    
    room_id: int
    facility_id: int
    room_name: str
    room_floor: str
    room_image: Optional[str]
    room_capacity: int
    room_equipment: Optional[str]
    use_tf: bool
    
    average_rating: float = 0.0
    review_count: int = 0

    reg_date: datetime
    up_date: datetime
    del_date: datetime
    
class StudyRoomListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room_id: int
    facility_id: int
    
    facility_item: FacilityDetailResponse
    review_items: List[ReviewListItemResponse] = []    

    room_name: str
    room_floor: str
    room_capacity: int
    room_equipment: str
    use_tf: bool
    
    average_rating: float = 0.0
    review_count: int = 0

class StudyRoomListResponse(BaseModel):
    items: List[StudyRoomListItemResponse]
    total_count: int
    
    
    
    
    
    

    
    
    


    
    


