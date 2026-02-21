from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.review import Review

class ReviewRepository:

    async def save(self, db: AsyncSession, entity: Review):
        db.add(entity)
        return entity

    async def find_by_id(self, db: AsyncSession, review_id: int):
        stmt = (
            select(Review)
            .where(Review.review_id == review_id)
            .options(
                selectinload(Review.student),
                selectinload(Review.room),
            )
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_plain_by_id(self, db: AsyncSession, review_id: int):
        stmt = select(Review).where(Review.review_id == review_id)
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_by_room_and_student(
        self,
        db: AsyncSession,
        room_id: int,
        student_id: int,
    ):
        stmt = (
            select(Review)
            .where(Review.room_id == room_id)
            .where(Review.student_id == student_id)
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_all_by_room_id(self, db: AsyncSession, room_id: int):
        stmt = (
            select(Review)
            .where(Review.room_id == room_id)
            .options(selectinload(Review.student))  # 목록에서 student_item 필요
            .order_by(Review.review_id.desc())
        )
        res = await db.execute(stmt)
        return res.scalars().all()

    async def get_room_rating_summary(self, db: AsyncSession, room_id: int):
        """스터디룸 목록/상세에서 평균별점/리뷰수 붙일 때 사용"""
        stmt = (
            select(
                func.coalesce(func.avg(Review.rating), 0).label("avg_rating"),
                func.count(Review.review_id).label("review_count"),
            )
            .where(Review.room_id == room_id)
        )
        res = await db.execute(stmt)
        return res.one()  # (avg_rating, review_count)

    async def delete(self, db: AsyncSession, entity: Review) -> None:
        await db.delete(entity)


review_repository = ReviewRepository()