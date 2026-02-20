# schemas/student.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict

class StudentCreate(BaseModel):
    student_no: str
    student_password: str
    student_name: str
    student_department : str
    student_phone : str

# schemas/student.py에 로그인 관련 스키마를 추가한다.
class StudentLogin(BaseModel):
    student_no: str
    student_password: str
    
# 전체 Detail Model 정의
class StudentDetail(BaseModel):
    student_id: int
    student_no: str
    student_name: str
    student_department : str
    student_phone : str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"