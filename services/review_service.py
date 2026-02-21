from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from models.review import Review
from models.study_room import StudyRoom
from repositories.review_repository import review_repository

from schemas.review import (
    ReviewCreate,
    ReviewCreateResponse,
    ReviewDetail,
    ReviewListItemResponse,
    ReviewListResponse,
)

class ReviewService:

    # 리뷰 등록
    async def create(
        self,
        db: AsyncSession,
        payload: ReviewCreate,
        student_id: int,
    ) -> ReviewCreateResponse:
        # 별점 점수 확인
        if payload.rating < 1 or payload.rating > 5:
            raise HTTPException(status_code=400, detail="별점은 1~5 사이여야 합니다.")

        # 스터디룸 존재 여부 확인
        room = await db.get(StudyRoom, payload.room_id)
        if not room:
            raise HTTPException(status_code=404, detail="존재하지 않는 스터디룸입니다.")

        # 동일 학생이 같은 방에 이미 리뷰 작성했는지 확인
        stmt = select(Review).where(
            Review.room_id == payload.room_id,
            Review.student_id == student_id,
        )
    
        res = await db.execute(stmt)
        exists = res.scalar_one_or_none()

        if exists:
            raise HTTPException(status_code=400, detail="이미 해당 스터디룸에 리뷰를 작성했습니다.")

        entity = Review(
            room_id=payload.room_id,
            student_id=student_id,
            rating=payload.rating,
            comment=payload.comment,
        )

        try:
            await review_repository.save(db, entity)
            await db.flush()
            await db.commit()
            await db.refresh(entity)

            return ReviewCreateResponse(review_id=entity.review_id)

        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="리뷰 등록 중 오류가 발생했습니다.")

    # 리뷰 상세 조회
    async def detail(
        self,
        db: AsyncSession,
        review_id: int,
    ) -> ReviewDetail:

        entity = await review_repository.find_by_id(db, review_id)
        if not entity:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        result = ReviewDetail.model_validate(entity)
        result.student_item = entity.student
        return result

    # 특정 방 리뷰 목록
    async def list_by_room(
        self,
        db: AsyncSession,
        room_id: int,
    ) -> ReviewListResponse:

        rows = await review_repository.find_all_by_room_id(db, room_id)

        items: list[ReviewListItemResponse] = []
        for row in rows:
            dto = ReviewListItemResponse.model_validate(row)
            dto.student_item = row.student
            items.append(dto)

        return ReviewListResponse(
            items=items,
            total_count=len(items),
        )

    # 리뷰 수정 (본인만)
    async def update(
        self,
        db: AsyncSession,
        review_id: int,
        rating: int | None,
        comment: str | None,
        student_id: int,
    ):

        entity = await review_repository.find_by_id(db, review_id)
        if not entity:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        if entity.student_id != student_id:
            raise HTTPException(status_code=403, detail="본인의 리뷰만 수정할 수 있습니다.")

        if rating is not None:
            if rating < 1 or rating > 5:
                raise HTTPException(status_code=400, detail="별점은 1~5 사이여야 합니다.")
            entity.rating = rating

        if comment is not None:
            entity.comment = comment

        try:
            await db.commit()
            return {"ok": True, "message": "리뷰가 수정되었습니다."}
        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="리뷰 수정 중 오류가 발생했습니다.")

    # 리뷰 삭제 (본인만)
    async def delete(
        self,
        db: AsyncSession,
        review_id: int,
        student_id: int,
    ):

        entity = await review_repository.find_by_id(db, review_id)
        if not entity:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

        if entity.student_id != student_id:
            raise HTTPException(status_code=403, detail="본인의 리뷰만 삭제할 수 있습니다.")

        try:
            await db.delete(entity)
            await db.commit()
            return {"ok": True, "message": "리뷰가 삭제되었습니다."}
        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="리뷰 삭제 중 오류가 발생했습니다.")


review_service = ReviewService()