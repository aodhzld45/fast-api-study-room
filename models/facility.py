from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, Boolean, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP

from configs.db import Base

if TYPE_CHECKING:
    from models.study_room import StudyRoom 

class Facility(Base):
    __tablename__ = "facility"

    facility_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    facility_name: Mapped[str] = mapped_column(String(100), nullable=False)
    facility_address: Mapped[str] = mapped_column(String(50), nullable=False)
    facility_desc: Mapped[str] = mapped_column(String(50), nullable=False)

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
    
    study_room_items: Mapped[list["StudyRoom"]] = relationship(
        "StudyRoom", 
        back_populates="facility", 
        lazy="selectin"
    )