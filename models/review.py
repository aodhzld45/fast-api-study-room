from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from configs.db import Base

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

    facility_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("facility.facility_id", ondelete="CASCADE"),
        nullable=False,
    )

    student_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("student.student_id", ondelete="CASCADE"),
        nullable=False,
    )

    rating: Mapped[float] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String(255), nullable=False)

    # room = relationship("StudyRoom", back_populates="reviews")
    # student = relationship("Student", back_populates="reviews")
