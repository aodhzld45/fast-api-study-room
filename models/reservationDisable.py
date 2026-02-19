from sqlalchemy import BigInteger, ForeignKey, Text, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.db import Base

class ReservationDisable(Base):
    __tablename__ = "reservation_disable"

    disable_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    room_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("study_room.room_id", ondelete="CASCADE"),
        nullable=False,
    )

    facility_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("facility.facility_id", ondelete="CASCADE"),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    disable_date: Mapped[object] = mapped_column(Date, nullable=False)
    disable_start_at: Mapped[object] = mapped_column(DateTime, nullable=False)
    disable_end_at: Mapped[object] = mapped_column(DateTime, nullable=False)

    room = relationship("StudyRoom")
    facility = relationship("Facility")
