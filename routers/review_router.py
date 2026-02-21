from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configs.db import get_db
from dependencies import get_current_user

from models.student import Student
from services.review_service import review_service

from schemas.review import (
    ReviewCreate,
    ReviewCreateResponse,
    ReviewDetail,
    ReviewListResponse,
)

router = APIRouter(
    prefix="/api/reviews",
    tags=["Review"],
)

@router.post(
    "",
    response_model=ReviewCreateResponse,
    summary="리뷰 등록",
)
async def create_review(
    payload: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user),
):
    return await review_service.create(
        db=db,
        payload=payload,
        student_id=current_user.student_id,
    )


@router.get(
    "/{review_id}",
    response_model=ReviewDetail,
    summary="리뷰 상세 조회",
)
async def get_review_detail(
    review_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await review_service.detail(
        db=db,
        review_id=review_id,
    )


@router.get(
    "/room/{room_id}",
    response_model=ReviewListResponse,
    summary="스터디룸 리뷰 목록 조회",
)
async def list_reviews_by_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await review_service.list_by_room(
        db=db,
        room_id=room_id,
    )


@router.patch(
    "/{review_id}",
    summary="리뷰 수정(본인만)",
)
async def update_review(
    review_id: int,
    payload: dict, 
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user),
):
    rating = payload.get("rating")
    comment = payload.get("comment")

    return await review_service.update(
        db=db,
        review_id=review_id,
        rating=rating,
        comment=comment,
        student_id=current_user.student_id,
    )


@router.delete(
    "/{review_id}",
    summary="리뷰 삭제(본인만)",
)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Student = Depends(get_current_user),
):
    return await review_service.delete(
        db=db,
        review_id=review_id,
        student_id=current_user.student_id,
    )