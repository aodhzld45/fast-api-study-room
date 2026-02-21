from sqlalchemy import BigInteger, ForeignKey, Integer, String, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from configs.db import Base

if TYPE_CHECKING:
    from models.study_room import StudyRoom
    from models.student import Student

class Review(Base):
    __tablename__ = "review"

    review_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    room_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("study_room.room_id", ondelete="CASCADE"),
        nullable=False,
    )

    student_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("student.student_id", ondelete="CASCADE"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1~5
    comment: Mapped[str] = mapped_column(String(255), nullable=False)
    
    reg_date: Mapped[object] = mapped_column(Date, nullable=False, server_default=func.current_date())

    room: Mapped["StudyRoom"] = relationship(
        "StudyRoom",
        back_populates="review_items",
    )

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="review_items",
    )