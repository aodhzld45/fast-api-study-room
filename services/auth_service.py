import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy.ext.asyncio import AsyncSession # AsyncSession으로 변경
from fastapi import HTTPException, status
from dotenv import load_dotenv

from repositories.student_repository import student_repository
from models.student import Student
from schemas.student import StudentCreate, StudentLogin

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

class AuthService:
    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, student_password: str, hashed: str) -> bool:
        return bcrypt.checkpw(student_password.encode("utf-8"), hashed.encode("utf-8"))

    # async 추가
    async def signup(self, db: AsyncSession, data: StudentCreate):
        async with db.begin(): # async with로 변경
            # 1. 학번 중복 검사 (await 추가)
            existing_student = await student_repository.find_by_student_no(db, data.student_no)
            if existing_student:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="이미 등록된 학번입니다.",
                )

            # 2. 비밀번호 해싱
            hashed_password = self.hash_password(data.student_password)

            # 3. 사용자 저장
            new_student = Student(
                student_no=data.student_no,
                student_password=hashed_password,
                student_name=data.student_name,
                student_department=data.student_department,
                student_phone=data.student_phone
            )
            await student_repository.save(db, new_student) # await 추가

        # db.refresh는 필요 시 비동기로 호출 (보통 save 내부에 flush가 있으면 생략 가능)
        return new_student
    
    # async 추가
    async def login(self, db: AsyncSession, data: StudentLogin) -> str:
        # 1. 학번으로 사용자 조회 (await 추가)
        student = await student_repository.find_by_student_no(db, data.student_no)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="학번 또는 비밀번호가 올바르지 않습니다.",
            )

        # 2. 비밀번호 검증
        if not self.verify_password(data.student_password, student.student_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="학번 또는 비밀번호가 올바르지 않습니다.",
            )

        # 3. JWT 토큰 생성
        access_token = self.create_access_token(student.student_id)
        return access_token

    def create_access_token(self, student_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
        payload = {
            "sub": str(student_id),
            "exp": expire,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # async 추가
    async def get_current_user(self, db: AsyncSession, token: str) -> Student:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            student_id_str = payload.get("sub")
            if student_id_str is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다.")
            student_id = int(student_id_str)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 만료되었거나 유효하지 않습니다.",
            )

        # await 추가
        student = await student_repository.find_by_id(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="학생을 찾을 수 없습니다.",
            )

        return student

auth_service = AuthService()
