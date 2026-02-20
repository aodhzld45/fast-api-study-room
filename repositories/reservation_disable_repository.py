from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.reservation_disable import ReservationDisable


class ReservationDisableRepository:
    async def find_disable(
        self,
        db: AsyncSession,
        room_id: int,
        reservation_date: date,
        start_dt: datetime,
        end_dt: datetime,
    ) -> ReservationDisable | None:
        stmt = (
            select(ReservationDisable)
            .where(ReservationDisable.room_id == room_id)
            .where(ReservationDisable.disable_date == reservation_date)
            .where(
                ReservationDisable.disable_start_at < end_dt,
                ReservationDisable.disable_end_at > start_dt,
            )
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_all_by_room_and_date(
        self,
        db: AsyncSession,
        room_id: int,
        disable_date: date,
    ) -> list[ReservationDisable]:
        stmt = (
            select(ReservationDisable)
            .where(ReservationDisable.room_id == room_id)
            .where(ReservationDisable.disable_date == disable_date)
            .order_by(ReservationDisable.disable_start_at.asc())
        )
        res = await db.execute(stmt)
        return res.scalars().all()


reservation_disable_repository = ReservationDisableRepository()