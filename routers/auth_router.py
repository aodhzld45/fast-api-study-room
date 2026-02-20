# routers/auth_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession # AsyncSession으로 변경
from configs.db import get_db
from services.auth_service import auth_service
from schemas.student import (
    StudentCreate,
    StudentDetail,
    TokenResponse,
    StudentLogin
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=StudentDetail, status_code=status.HTTP_201_CREATED)
async def signup(data: StudentCreate, db: AsyncSession = Depends(get_db)): # async 및 AsyncSession 적용
    return await auth_service.signup(db, data)

@router.post("/login", response_model=TokenResponse)
async def login(data: StudentLogin, db: AsyncSession = Depends(get_db)): # async 및 AsyncSession 적용
    access_token = await auth_service.login(db, data)
    return {"access_token": access_token, "token_type": "bearer"}
