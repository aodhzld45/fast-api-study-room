from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from configs.db import get_db
from services.auth_service import auth_service
from models.student import Student

# Authorization 헤더에서 Bearer 토큰을 자동으로 추출한다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession  = Depends(get_db),
) -> Student:
    return await auth_service.get_current_user(db, token)