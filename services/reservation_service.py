from datetime import date, datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlalchemy.exc import SQLAlchemyError

from models.facility import Facility
from models.study_room import StudyRoom
from models.reservation import Reservation

from repositories.reservation_repository import reservation_repository
from repositories.reservation_disable_repository import reservation_disable_repository

from schemas.reservation import (
    ReservationCreate,
    ReservationCreateResponse,
    ReservationDetail,
    ReservationListItemResponse,
    ReservationListResponse,
)

logger = logging.getLogger(__name__)

class ReservationService:
    async def create(self, db: AsyncSession, payload: ReservationCreate, student_id: int) -> ReservationCreateResponse:
        try:
            # 0) 기본 참조 데이터 확인
            target_room = await db.get(StudyRoom, payload.room_id)
            if not target_room:
                raise HTTPException(status_code=404, detail="선택한 스터디룸을 찾을 수 없습니다. 다시 선택해 주세요.")

            target_facility = await db.get(Facility, payload.facility_id)
            if not target_facility:
                raise HTTPException(status_code=404, detail="선택한 시설 정보를 확인할 수 없습니다. 다시 시도해 주세요.")

            # 1) 방-시설 매칭 검증
            if target_room.facility_id != payload.facility_id:
                raise HTTPException(status_code=400, detail="선택한 방이 해당 시설에 속하지 않습니다. 방/시설을 다시 확인해 주세요.")

            # 2) 예약 가능 날짜(오늘~7일)
            today = date.today()
            last_allowed = today + timedelta(days=7)
            if payload.reservation_date < today or payload.reservation_date > last_allowed:
                raise HTTPException(status_code=400, detail="예약은 오늘부터 최대 7일 이내 날짜만 가능합니다.")

            # 3) 시간 유효성
            start_at = payload.reservation_start_date
            end_at = payload.reservation_end_date

            if start_at.date() != payload.reservation_date or end_at.date() != payload.reservation_date:
                raise HTTPException(status_code=400, detail="예약일(reservation_date)과 시작/종료 시간이 동일한 날짜여야 합니다.")
            if end_at <= start_at:
                raise HTTPException(status_code=400, detail="종료 시간은 시작 시간 이후로 설정해 주세요.")

            # 4) 1시간/2시간 단위만 허용
            duration_minutes = int((end_at - start_at).total_seconds() // 60)
            if duration_minutes not in (60, 120):
                raise HTTPException(status_code=400, detail="예약 시간은 1시간 또는 2시간 단위로만 선택할 수 있습니다.")

            # 5) 운영시간 검증 (필드가 존재할 때만)
            if hasattr(target_room, "open_time") and hasattr(target_room, "close_time"):
                start_time = start_at.time()
                end_time = end_at.time()
                if start_time < target_room.open_time or end_time > target_room.close_time:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"해당 스터디룸은 {target_room.open_time.strftime('%H:%M')} ~ "
                            f"{target_room.close_time.strftime('%H:%M')} 사이에만 예약할 수 있습니다."
                        ),
                    )

            # 6) 하루 최대 2시간 제한(합산)
            request_count = 1 if duration_minutes == 60 else 2
            already_used = await reservation_repository.sum_count_by_student_and_date(db, student_id, payload.reservation_date)
            already_used = int(already_used or 0)
            if already_used + request_count > 2:
                raise HTTPException(status_code=400, detail="하루 최대 이용 가능 시간(2시간)을 초과했습니다.")

            # 7) 사용자 예약 시간 중복 체크(다른 방 포함)
            user_overlap = await reservation_repository.find_user_disable(db, student_id, payload.reservation_date, start_at, end_at)
            if user_overlap:
                raise HTTPException(status_code=409, detail="선택한 시간에 이미 예약이 존재합니다. 다른 시간을 선택해 주세요.")

            # 8) 동일 방 예약 시간 중복 체크
            room_overlap = await reservation_repository.find_room_disable(db, payload.room_id, payload.reservation_date, start_at, end_at)
            if room_overlap:
                raise HTTPException(status_code=409, detail="해당 시간은 이미 예약이 완료되었습니다. 다른 시간을 선택해 주세요.")

            # 9) 관리자 차단 시간 중복 체크
            blocked_overlap = await reservation_disable_repository.find_disable(db, payload.room_id, payload.reservation_date, start_at, end_at)
            if blocked_overlap:
                raise HTTPException(status_code=409, detail="해당 시간은 예약이 제한되어 있습니다. 다른 시간을 선택해 주세요.")

            # 10) 저장
            entity = Reservation(
                student_id=student_id,
                room_id=payload.room_id,
                facility_id=payload.facility_id,
                reservation_status="예약완료",
                reservation_date=payload.reservation_date,
                reservation_start_date=start_at,
                reservation_end_date=end_at,
                reservation_count=request_count,
                use_tf=payload.use_tf,
            )

            await reservation_repository.save(db, entity)  # db.add
            await db.flush()      # PK 생성
            await db.commit()     # 실제 반영
            await db.refresh(entity)

            return ReservationCreateResponse(reservation_id=entity.reservation_id)

        except HTTPException:
            raise

        except SQLAlchemyError:
            await db.rollback()
            logger.exception("DB error on POST /reservations")
            raise HTTPException(status_code=500, detail="예약 처리 중 DB 오류가 발생했습니다.")

        except Exception:
            await db.rollback()
            logger.exception("Unexpected error on POST /reservations")
            raise HTTPException(status_code=500, detail="예약 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")


    async def detail(self, db: AsyncSession, reservation_id: int) -> ReservationDetail:
        entity = await reservation_repository.find_by_id_with_items(db, reservation_id)
        if not entity:
            raise HTTPException(status_code=404, detail="요청하신 예약 정보를 찾을 수 없습니다.")

        result = ReservationDetail.model_validate(entity)
        result.student_item = getattr(entity, "student", None)
        result.room_item = getattr(entity, "room", None)
        result.facility_item = getattr(entity, "facility", None)
        return result

    async def list_by_student(self, db: AsyncSession, student_id: int) -> ReservationListResponse:
        rows = await reservation_repository.find_all_by_student_id_with_items(db, student_id)

        items: list[ReservationListItemResponse] = []
        for row in rows:
            dto = ReservationListItemResponse.model_validate(row)
            dto.student_item = getattr(row, "student", None)
            dto.room_item = getattr(row, "room", None)
            dto.facility_item = getattr(row, "facility", None)
            items.append(dto)

        return ReservationListResponse(items=items, total_count=len(items))

    async def cancel(self, db: AsyncSession, reservation_id: int, student_id: int):
        entity = await reservation_repository.find_by_id(db, reservation_id)
        if not entity:
            raise HTTPException(status_code=404, detail="취소하려는 예약이 존재하지 않습니다.")

        if entity.student_id != student_id:
            raise HTTPException(status_code=403, detail="본인의 예약만 취소할 수 있습니다.")

        if entity.reservation_status != "예약완료":
            raise HTTPException(status_code=400, detail="현재 상태에서는 예약을 취소할 수 없습니다.")

        if datetime.now() >= entity.reservation_start_date - timedelta(hours=1):
            raise HTTPException(status_code=400, detail="예약 취소는 시작 1시간 전까지만 가능합니다.")

        async with db.begin():
            entity.reservation_status = "취소"
            entity.cancel_date = date.today()

        return {"ok": True, "message": "예약이 정상적으로 취소되었습니다."}


reservation_service = ReservationService()