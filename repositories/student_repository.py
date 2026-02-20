from sqlalchemy import select
from models.student import Student
from sqlalchemy.ext.asyncio import AsyncSession

class Studentrepository:
    async def save(self, db: AsyncSession, student: Student):
        db.add(student)
        return student
    
    async def find_by_student_no(self, db: AsyncSession, student_no: str):
        stmt = select(Student).where(Student.student_no == student_no)
        result = await db.scalars(stmt) 
        return result.first()

    async def find_by_id(self, db: AsyncSession, student_id: int):
        return await db.get(Student, student_id)
    
    
student_repository = Studentrepository()


