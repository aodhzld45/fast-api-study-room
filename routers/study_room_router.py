from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_db
from schemas.study_room import (
    StudyRoomCreate,
    StudyRoomCreateResponse,
    StudyRoomDetail,
    StudyRoomListResponse,
)

from services.study_room_service import study_room_service

router = APIRouter(prefix="/api/study-rooms", tags=["study-rooms"])

@router.post("", response_model=StudyRoomCreateResponse)
async def create_facility(
    req: StudyRoomCreate,
    db: AsyncSession = Depends(get_db),
):
    return await study_room_service.create(db, req)

@router.get("/{room_id}", response_model=StudyRoomDetail)
async def read_study_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await study_room_service.detail(db, room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=StudyRoomListResponse)
async def list_study_rooms(
    facilityId: int = Query(None, description="시설 ID (facility_id)"),
    room_floor: str = Query(None, description="층 (room_floor)"),
    room_capacity: int = Query(None, description="총 수용인원" ),
    db: AsyncSession = Depends(get_db),
):
    # /api/study-rooms?facilityId=1
    return await study_room_service.list_by_facility(db, facilityId, room_floor, room_capacity)






