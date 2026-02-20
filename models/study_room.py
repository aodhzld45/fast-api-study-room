from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP

from configs.db import Base

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

    # 관계: Facility 쪽에도 relationship 걸면 양방향 가능
    facility_item = relationship("Facility", lazy="selectin")
