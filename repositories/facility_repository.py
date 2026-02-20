# /repositories/facility_repository.py

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.facility import Facility


class FacilityRepository:
    async def save(self, db: AsyncSession, facility: Facility) -> Facility:
        db.add(facility)
        return facility

    async def find_by_id(self, db: AsyncSession, facility_id: int) -> Facility | None:
        # 단순 조회 (관계 로딩 필요 없을 때)
        return await db.get(Facility, facility_id)

    async def find_by_id_with_study_rooms(
        self, db: AsyncSession, facility_id: int
    ) -> Facility | None:
        # detail에서 쓰는 버전 (study_room selectinload)
        stmt = (
            select(Facility)
            .where(Facility.facility_id == facility_id)
            .options(selectinload(Facility.study_room))
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_all(self, db: AsyncSession) -> list[Facility]:
        stmt = select(Facility).order_by(Facility.facility_id.desc())
        res = await db.execute(stmt)
        return res.scalars().all()

    async def count_all(self, db: AsyncSession) -> int:
        stmt = select(func.count()).select_from(Facility)
        total = await db.scalar(stmt)
        return int(total or 0)


facility_repository = FacilityRepository()