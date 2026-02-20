from fastapi import FastAPI
# DB 연결 설정 부분
from configs.db import ping_db, Base, engine
from contextlib import asynccontextmanager

from routers.student_router import router as student_router
from routers.auth_router import router as auth_router

import models

# 비동기 방식의 DB 자동 DDL 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 비동기 엔진에서 동기 메서드(create_all)를 실행하는 방법
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(student_router)
app.include_router(auth_router)

@app.get("/health/db")
async def health_db():
    ok = await ping_db()
    return {"ok": ok}

