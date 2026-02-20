# app/repositories/study_room_repository.py
from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload

from models.study_room import StudyRoom

class StudyRoomRepository:
    async def save(self, db: AsyncSession, study_room: StudyRoom) -> StudyRoom:
        db.add(study_room)
        return study_room

    async def find_by_id(self, db: AsyncSession, room_id: int) -> StudyRoom | None:
        return await db.get(StudyRoom, room_id)

    async def find_all_by_facility_id(
        self,
        db: AsyncSession,
        facility_id: int,
        room_floor: str | None = None,   
        room_capacity: int | None = None
    ) -> list[StudyRoom]:
        # 1. 기본 쿼리: 특정 시설(facility_id)의 데이터는 무조건 가져옴
        stmt = (
            select(StudyRoom)
            .options(joinedload(StudyRoom.facility_item)) 
            .where(StudyRoom.facility_id == facility_id)
        )
        
        # 2. 층수 필터: "전체"가 아닐 때만 조건 추가
        # 만약 프론트에서 "전체 층" 선택 시 빈 문자열("")을 보낸다면 아래와 같이 체크
        if room_floor and room_floor != "전체":
            stmt = stmt.where(StudyRoom.room_floor == room_floor)
            
        # 3. 인원수 필터: 입력된 인원 이상 수용 가능한 방을 보여주는 것이 일반적입니다.
        # 인원수가 0보다 클 때만 필터링 (0은 보통 전체 인원을 의미하도록 설계)
        if room_capacity and room_capacity > 0:
            # 이미지처럼 '최대 4명'인 방에 4명이 들어가려면 capacity가 4 이상이어야 함
            stmt = stmt.where(StudyRoom.room_capacity >= room_capacity)
            
        # 4. 정렬
        stmt = stmt.order_by(StudyRoom.room_id.desc())

        res = await db.execute(stmt)
        return res.scalars().all()

    async def count_all(self, db: AsyncSession) -> int:
        stmt = select(func.count()).select_from(StudyRoom)
        total = await db.scalar(stmt)
        return int(total or 0)

    async def count_by_facility_id(self, db: AsyncSession, facility_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(StudyRoom)
            .where(StudyRoom.facility_id == facility_id)
        )
        total = await db.scalar(stmt)
        return int(total or 0)


study_room_repository = StudyRoomRepository()