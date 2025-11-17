from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Mentor
from schemas import MentorResponse

router = APIRouter()

@router.get("/", response_model=List[MentorResponse])
def get_mentors(db: Session = Depends(get_db)):
    """Lấy danh sách tất cả mentors đang active"""
    mentors = db.query(Mentor).filter(Mentor.isActive == True).all()
    return mentors

@router.get("/{mentor_id}", response_model=MentorResponse)
def get_mentor(mentor_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin mentor theo ID"""
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id, Mentor.isActive == True).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor không tồn tại")
    return mentor

