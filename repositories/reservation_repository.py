from datetime import date, datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.reservation import Reservation


class ReservationRepository:
    async def save(self, db: AsyncSession, reservation: Reservation):
        db.add(reservation)
        return reservation

    async def find_by_id(self, db: AsyncSession, reservation_id: int) -> Reservation | None:
        stmt = select(Reservation).where(Reservation.reservation_id == reservation_id)
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_by_id_with_items(self, db: AsyncSession, reservation_id: int) -> Reservation | None:
        stmt = (
            select(Reservation)
            .where(Reservation.reservation_id == reservation_id)
            .options(
                selectinload(Reservation.student),
                selectinload(Reservation.room),
                selectinload(Reservation.facility),
            )
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_by_user_id(self, db: AsyncSession, user_id: int) -> list[Reservation]:
        stmt = (
            select(Reservation)
            .where(Reservation.student_id == user_id)
            .order_by(Reservation.reservation_date.desc(), Reservation.reservation_start_date.desc())
        )
        res = await db.execute(stmt)
        return res.scalars().all()

    async def find_all_by_student_id(self, db: AsyncSession, student_id: int) -> list[Reservation]:
        return await self.find_by_user_id(db, student_id)

    async def find_all_by_student_id_with_items(self, db: AsyncSession, student_id: int) -> list[Reservation]:
        stmt = (
            select(Reservation)
            .where(Reservation.student_id == student_id)
            .options(
                selectinload(Reservation.student),
                selectinload(Reservation.room),
                selectinload(Reservation.facility),
            )
            .order_by(Reservation.reservation_date.desc(), Reservation.reservation_start_date.desc())
        )
        res = await db.execute(stmt)
        return res.scalars().all()

    async def count_by_user_and_date(self, db: AsyncSession, user_id: int, reservation_date: date) -> int:
        stmt = (
            select(func.count())
            .select_from(Reservation)
            .where(Reservation.student_id == user_id)
            .where(Reservation.reservation_date == reservation_date)
            .where(Reservation.reservation_status == "예약완료")
        )
        total = await db.scalar(stmt)
        return int(total or 0)

    async def sum_count_by_student_and_date(self, db: AsyncSession, student_id: int, reservation_date: date) -> int:
        stmt = (
            select(func.coalesce(func.sum(Reservation.reservation_count), 0))
            .select_from(Reservation)
            .where(Reservation.student_id == student_id)
            .where(Reservation.reservation_date == reservation_date)
            .where(Reservation.reservation_status == "예약완료")
        )
        total = await db.scalar(stmt)
        return int(total or 0)

    async def find_room_disable(
        self,
        db: AsyncSession,
        room_id: int,
        reservation_date: date,
        start_dt: datetime,
        end_dt: datetime,
    ) -> Reservation | None:
        # 같은 room에서 시간 겹치는 예약이 있는지
        stmt = (
            select(Reservation)
            .where(Reservation.room_id == room_id)
            .where(Reservation.reservation_date == reservation_date)
            .where(Reservation.reservation_status == "예약완료")
            .where(
                Reservation.reservation_start_date < end_dt,
                Reservation.reservation_end_date > start_dt,
            )
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_user_disable(
        self,
        db: AsyncSession,
        user_id: int,
        reservation_date: date,
        start_dt: datetime,
        end_dt: datetime,
    ) -> Reservation | None:
        stmt = (
            select(Reservation)
            .where(Reservation.student_id == user_id)
            .where(Reservation.reservation_date == reservation_date)
            .where(Reservation.reservation_status == "예약완료")
            .where(
                Reservation.reservation_start_date < end_dt,
                Reservation.reservation_end_date > start_dt,
            )
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    async def find_disable(
        self,
        db: AsyncSession,
        room_id: int,
        reservation_date: date,
        start_dt: datetime,
        end_dt: datetime,
    ) -> Reservation | None:
        return await self.find_room_conflict(db, room_id, reservation_date, start_dt, end_dt)


reservation_repository = ReservationRepository()