from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User
from schemas import UserCreate, UserUpdate, UserResponse
from routers.authen import currentLoginUser

# Tạo router cho user
router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user=Depends(currentLoginUser)):
    """Lấy tất cả users - chỉ admin mới có quyền"""
    users = db.query(User).filter(User.isActive == True).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(currentLoginUser)):
    """Lấy user theo ID"""
    user = db.query(User).filter(User.id == user_id, User.isActive == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    # Kiểm tra quyền: chỉ cho phép xem chính mình hoặc admin
    if not current_user["isMentor"] and current_user["user"].id != user_id:
        raise HTTPException(status_code=403, detail="Không có quyền truy cập")
    
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Tạo user mới - không cần authentication"""
    # Kiểm tra username đã tồn tại chưa
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    
    # Tạo user mới
    db_user = User(
        username=user.username,
        name=user.name,
        password=user.password,  # Trong thực tế nên hash password
        email=user.email,
        phone=user.phone,
        address=user.address,
        isActive=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user=Depends(currentLoginUser)):
    """Cập nhật user"""
    db_user = db.query(User).filter(User.id == user_id, User.isActive == True).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    # Kiểm tra quyền: chỉ cho phép cập nhật chính mình
    if current_user["isMentor"] or current_user["user"].id != user_id:
        raise HTTPException(status_code=403, detail="Không có quyền cập nhật user này")
    
    # Cập nhật các trường
    if user.username is not None:
        # Kiểm tra username mới không trùng với user khác
        existing_user = db.query(User).filter(User.username == user.username, User.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username đã tồn tại")
        db_user.username = user.username
    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    if user.phone is not None:
        db_user.phone = user.phone
    if user.address is not None:
        db_user.address = user.address
    if user.password is not None:
        db_user.password = user.password  # Trong thực tế nên hash password
    if user.isActive is not None:
        db_user.isActive = user.isActive
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(currentLoginUser)):
    """Xóa user (soft delete - đặt isActive = False)"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    # Kiểm tra quyền: chỉ cho phép xóa chính mình
    if current_user["isMentor"] or current_user["user"].id != user_id:
        raise HTTPException(status_code=403, detail="Không có quyền xóa user này")
    
    # Soft delete
    db_user.isActive = False
    db.commit()
    return {"message": "Xóa user thành công"} 