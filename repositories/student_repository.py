from sqlalchemy import select
from models.student import Student
from sqlalchemy.ext.asyncio import AsyncSession

class Studentrepository:
    async def save(self, db: AsyncSession, user: Student):
        db.add(user)
        return user

    async def find_by_email(self, db: AsyncSession, email: str):
        stmt = select(Student).where(Student.email == email)
        return db.scalars(stmt).first()

    async def find_by_id(self, db: AsyncSession, user_id: int):
        return db.get(Student, user_id)
    
student_repository = Studentrepository()