# services/auth_service.py
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from dotenv import load_dotenv

from repositories.user2_repository import user2_repository
from models.user2 import User2
from schemas.user2 import User2Create, User2Login

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

class AuthService:
    def _hash_password(self, password: str) -> str:
        """비밀번호를 bcrypt로 해싱한다."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def signup(self, db: Session, data: User2Create):
        with db.begin():
            # 1. 이메일 중복 검사
            existing_user = user2_repository.find_by_email(db, data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="이미 등록된 이메일입니다.",
                )

            # 2. 비밀번호 해싱
            hashed_password = self._hash_password(data.password)

            # 3. 사용자 저장
            new_user = User2(email=data.email, nickname=data.nickname, password=hashed_password)
            user2_repository.save(db, new_user)

        db.refresh(new_user)

        return new_user
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """입력된 비밀번호와 해시된 비밀번호를 비교한다."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        
    def login(self, db: Session, data: User2Login) -> str:
        # 1. 이메일로 사용자 조회
        user = user2_repository.find_by_email(db, data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        # 2. 비밀번호 검증
        if not self._verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        # 3. JWT 토큰 생성
        access_token = self._create_access_token(user.id)
        return access_token

    def _create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "exp": expire,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # ===============토큰 검증 로직 ================
    def get_current_user(self, db: Session, token: str) -> User2:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = int(payload.get("sub"))

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="유효하지 않은 토큰입니다.",
                )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 만료되었습니다.",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다.",
            )

        user = user2_repository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="사용자를 찾을 수 없습니다.",
            )

        return user

auth_service = AuthService()