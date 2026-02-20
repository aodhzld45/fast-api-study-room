from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_db
from dependencies import get_current_user 

from models.student import Student 
from services.reservation_service import reservation_service

from schemas.reservation import (
    ReservationCreate,
    ReservationCreateResponse,
    ReservationDetail,
    ReservationListResponse,
)

router = APIRouter(
    prefix="/api/reservations",
    tags=["Reservation"],
)

@router.post(
    "",
    response_model=ReservationCreateResponse,
    summary="예약 신청",
)
async def create_reservation(
    payload: ReservationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user), 
):
    return await reservation_service.create(
        db,
        payload,
        current_user.student_id, 
    )
    
@router.get(
    "/me",
    response_model=ReservationListResponse,
    summary="내 예약 목록 조회",
)
async def get_my_reservations(
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user),
):
    return await reservation_service.list_by_student(
        db,
        current_user.student_id, 
    )

@router.get(
    "/{reservation_id}",
    response_model=ReservationDetail,
    summary="예약 상세 조회",
)
async def get_reservation_detail(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user),
):
    return await reservation_service.detail(db, reservation_id)




@router.patch(
    "/{reservation_id}/cancel",
    summary="예약 취소",
)
async def cancel_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user),
):
    return await reservation_service.cancel(
        db,
        reservation_id,
        current_user.student_id,
    )