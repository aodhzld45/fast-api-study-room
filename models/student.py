from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from configs.db import Base

class Student(Base):
    __tablename__ = "student"

    student_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    
    student_no: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)  
    student_password: Mapped[str] = mapped_column(String(255), nullable=False)
    student_name: Mapped[str] = mapped_column(String(10), nullable=False)
    student_department: Mapped[str] = mapped_column(String(50), nullable=False)
    student_phone: Mapped[str] = mapped_column(String(50), nullable=False)