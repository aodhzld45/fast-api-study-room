from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from configs.db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.facility import Facility
    from models.review import Review

class StudyRoom(Base):
    __tablename__ = "study_room"

    room_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    facility_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("facility.facility_id", ondelete="RESTRICT"),
        nullable=False,
    )

    room_name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    room_floor: Mapped[str] = mapped_column(String(50), nullable=False)

    room_image: Mapped[str | None] = mapped_column(Text, nullable=True)  # file path
    room_capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    room_equipment: Mapped[str | None] = mapped_column(String(50), nullable=True)

    use_tf: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    reg_date: Mapped[object] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    up_date: Mapped[object] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    del_date: Mapped[object] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    facility_item: Mapped["Facility"] = relationship(
        "Facility", 
        back_populates="study_room_items"
    )
    
    review_items: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="room",
        cascade="all, delete-orphan",
    )
