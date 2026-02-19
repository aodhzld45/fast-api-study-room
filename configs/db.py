from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from .config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# SQLAlchemy 2.0 스타일의 Base 클래스 선언
class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def ping_db() -> bool:
    async with AsyncSessionLocal() as session:
        await session.execute(text("select 1"))
    return True
