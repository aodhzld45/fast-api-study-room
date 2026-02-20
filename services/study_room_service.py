# /services/study_room_service.py
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.study_room_repository import study_room_repository

from models.facility import Facility
from models.study_room import StudyRoom
from schemas.study_room import (
    StudyRoomCreate,
    StudyRoomCreateResponse,
    StudyRoomDetail,
    StudyRoomListItemResponse,
    StudyRoomListResponse
)

class StudyRoomServices:
    async def create(self, db: AsyncSession, req: StudyRoomCreate) -> StudyRoomCreateResponse:
        # 1) facility 존재 확인
        facility = await db.get(Facility, req.facility_id)
        if not facility:
            raise ValueError(f"Facility not found. facility_id={req.facility_id}")

        # 2) StudyRoom 생성 + 관계 연결
        e = StudyRoom(
            facility_id=req.facility_id,
            room_name=req.room_name,
            room_floor=req.room_floor,
            room_image=req.room_image,
            room_capacity=req.room_capacity,
            room_equipment=req.room_equipment,
            use_tf=req.use_tf,
        )
        e.facility = facility

        await study_room_repository.save(db, e)
        await db.commit()
        await db.refresh(e)

        return StudyRoomCreateResponse(room_id=e.room_id)
    
    
    async def detail(self, db: AsyncSession, room_id: int) -> StudyRoomDetail:
        e = await study_room_repository.find_by_id(db, room_id)
        if not e:
            raise ValueError(f"StudyRoom not found. id={room_id}")

        return StudyRoomDetail.model_validate(e)

    async def list_by_facility(
        self,
        db: AsyncSession,
        facility_id: int,
        room_floor: str,
        room_capacity: int
        ) -> StudyRoomListResponse:
        rows = await study_room_repository.find_all_by_facility_id(db, facility_id, room_floor, room_capacity)

        items = [StudyRoomListItemResponse.model_validate(x) for x in rows]
        return StudyRoomListResponse(items=items, total_count=len(items))
    
study_room_service = StudyRoomServices()