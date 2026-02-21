from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from configs.db import get_db
from schemas.student import StudentDetail
# from schemas.post2 import Post2ListResponse - TO-BE 예약 reservation
from models.student import Student
from dependencies import get_current_user
# from services.auth_service import student_service

router = APIRouter(prefix="/student" ,tags=["ME"])

@router.get("/me", response_model=StudentDetail)
async def get_me(
    current_user: Student = Depends(get_current_user)):
    return current_user

# @router.get("/me/posts", response_model=list[Post2ListResponse])
# def read_my_posts(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     """내가 예약한 스터디룸 목록 조회"""
#     return student_service.read_posts_by_user_id(db, current_user.id)
    
    
# @router.get("/users/{user_id}/posts", response_model=list[Post2ListResponse])
# def read_posts_by_user(user_id: int, db: Session = Depends(get_db)):
#     """특정 학생이 에약한 스터디룸 목록 조회"""
#     return student_service.read_posts_by_user_id(db, user_id)
