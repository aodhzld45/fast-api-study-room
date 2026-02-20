# Reservation API Test Cases (간략)

## 공통
- Header: `Authorization: Bearer <TOKEN>` (또는 세션/쿠키)
- `Content-Type: application/json`

---

## 1) 예약 신청 `POST /reservations`

### TC-POST-01 성공 (1시간)
```json
{
  "facility_id": 1,
  "room_id": 3,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-20T14:00:00",
  "reservation_end_date": "2026-02-20T15:00:00",
  "use_tf": "Y"
}

TC-POST-02 실패 (1/2시간 단위 아님)

기대: 400 "예약 시간은 1시간 또는 2시간 단위..."

{
  "facility_id": 1,
  "room_id": 3,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-20T14:00:00",
  "reservation_end_date": "2026-02-20T15:30:00",
  "use_tf": "Y"
}

TC-POST-03 실패 (종료<=시작)

기대: 400 "종료 시간은 시작 시간 이후..."

{
  "facility_id": 1,
  "room_id": 3,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-20T15:00:00",
  "reservation_end_date": "2026-02-20T15:00:00",
  "use_tf": "Y"
}

TC-POST-04 실패 (예약일 범위 위반: 오늘~7일)

기대: 400 "예약은 오늘부터 최대 7일 이내..."

{
  "facility_id": 1,
  "room_id": 3,
  "reservation_date": "2026-01-01",
  "reservation_start_date": "2026-01-01T14:00:00",
  "reservation_end_date": "2026-01-01T15:00:00",
  "use_tf": "Y"
}

TC-POST-05 실패 (reservation_date와 start/end 날짜 불일치)

기대: 400 "예약일(reservation_date)과 시작/종료 시간이 동일한 날짜..."

{
  "facility_id": 1,
  "room_id": 3,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-21T14:00:00",
  "reservation_end_date": "2026-02-21T15:00:00",
  "use_tf": "Y"
}

TC-POST-06 실패 (하루 2시간 초과)

사전조건: 같은 날짜에 이미 reservation_count 합이 2

기대: 400 "하루 최대 이용 가능 시간(2시간)을 초과..."

{
  "facility_id": 1,
  "room_id": 4,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-20T18:00:00",
  "reservation_end_date": "2026-02-20T19:00:00",
  "use_tf": "Y"
}

TC-POST-07 실패 (사용자 시간 중복: 다른 방이어도)

사전조건: 14:00~15:00 예약 존재

기대: 409 "선택한 시간에 이미 예약이 존재..."

{
  "facility_id": 1,
  "room_id": 4,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-20T14:30:00",
  "reservation_end_date": "2026-02-20T15:30:00",
  "use_tf": "Y"
}

TC-POST-08 실패 (방 시간 중복: 같은 방)

사전조건: room_id=3 14:00~15:00 예약 존재

기대: 409 "해당 시간은 이미 예약이 완료..."

{
  "facility_id": 1,
  "room_id": 3,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-20T14:30:00",
  "reservation_end_date": "2026-02-20T15:30:00",
  "use_tf": "Y"
}

TC-POST-09 실패 (관리자 차단 시간)

사전조건: reservation_disable에 해당 시간 차단 존재

기대: 409 "해당 시간은 예약이 제한..."

{
  "facility_id": 1,
  "room_id": 3,
  "reservation_date": "2026-02-20",
  "reservation_start_date": "2026-02-20T15:00:00",
  "reservation_end_date": "2026-02-20T16:00:00",
  "use_tf": "Y"
}
















### ERD 링크 - https://www.erdcloud.com/d/D3F4APDLCyvpMNKtn