# /services/facility_service.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.facility import Facility
from schemas.facility import (
    FacilityCreate,
    FacilityCreateResponse,
    FacilityDetailResponse,
    FacilityListResponse,
    FacilityListItemResponse,
)

class FacilityService:
    async def create(self,db: AsyncSession, req: FacilityCreate) -> FacilityCreateResponse:
        e = Facility(
            facility_name=req.facility_name,
            facility_address=req.facility_address,
            facility_desc=req.facility_desc,
            use_tf=req.use_tf,
        )
        db.add(e)
        await db.commit()
        # PK/DEFAULT 컬럼 다시 로딩
        await db.refresh(e)

        return FacilityCreateResponse(facility_id=e.facility_id)

    async def detail(self, db: AsyncSession, facility_id: int) -> FacilityDetailResponse:
        stmt = (
            select(Facility)
            .where(Facility.facility_id == facility_id)
            .options(selectinload(Facility.study_room))
        )
        res = await db.execute(stmt)
        e = res.scalar_one_or_none()
        if not e:
            raise ValueError(f"Facility not found. id={facility_id}")

        return FacilityDetailResponse.model_validate(e)

    async def list(self, db: AsyncSession) -> FacilityListResponse:
        # 목록
        stmt = select(Facility).order_by(Facility.facility_id.desc())
        res = await db.execute(stmt)
        rows = res.scalars().all()

        # total count
        count_stmt = select(func.count()).select_from(Facility)
        total = await db.scalar(count_stmt)
        total = int(total or 0)

        items = [FacilityListItemResponse.model_validate(x) for x in rows]
        return FacilityListResponse(items=items, total_count=total)
    
facility_service = FacilityService()