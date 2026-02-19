from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.db import Base

class Reservation(Base):
    __tablename__ = "reservation"

    reservation_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    student_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("student.student_id", ondelete="RESTRICT"),
        nullable=False,
    )

    room_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("study_room.room_id", ondelete="RESTRICT"),
        nullable=False,
    )

    facility_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("facility.facility_id", ondelete="RESTRICT"),
        nullable=False,
    )

    reservation_status: Mapped[str] = mapped_column(String(20), nullable=False)

    reservation_date: Mapped[object] = mapped_column(Date, nullable=False)

    reservation_start_date: Mapped[object] = mapped_column(DateTime, nullable=False)
    reservation_end_date: Mapped[object] = mapped_column(DateTime, nullable=False)

    reservation_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    use_tf: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    # ERD가 DATE로 되어있어서 Date로 맞춤
    reg_date: Mapped[object] = mapped_column(Date, nullable=False, server_default=func.current_date())
    up_date: Mapped[object] = mapped_column(Date, nullable=False, server_default=func.current_date(), onupdate=func.current_date())
    del_date: Mapped[object] = mapped_column(Date, nullable=False, server_default=func.current_date())
    cancel_date: Mapped[object | None] = mapped_column(Date, nullable=True)

    # relationships
    student = relationship("Student", lazy="selectin")
    room = relationship("StudyRoom", lazy="selectin")
    facility = relationship("Facility", lazy="selectin")
