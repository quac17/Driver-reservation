from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Car
from schemas import CarResponse

router = APIRouter()

@router.get("/", response_model=List[CarResponse])
def get_cars(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lấy danh sách tất cả cars đang active, có thể filter theo status"""
    query = db.query(Car).filter(Car.isActive == True)
    
    if status:
        query = query.filter(Car.status == status)
    
    cars = query.all()
    return cars

@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin car theo ID"""
    car = db.query(Car).filter(Car.id == car_id, Car.isActive == True).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car không tồn tại")
    return car

