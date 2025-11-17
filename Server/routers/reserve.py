from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from database import get_db
from models import Reserve, ReserveDetail, User, Mentor, Car
from schemas import ReserveResponse, ReserveCreate, ReserveDetailResponse
from routers.authen import currentLoginUser

router = APIRouter()

@router.get("/", response_model=List[ReserveResponse])
def get_reserves(
    user_id: int = None,
    mentor_id: int = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(currentLoginUser)
):
    """Lấy danh sách reserves, có thể filter theo user_id, mentor_id, status"""
    query = db.query(Reserve)
    
    # Nếu là user, chỉ cho xem reserves của chính mình
    if not current_user["isMentor"]:
        query = query.filter(Reserve.user_id == current_user["user"].id)
    elif user_id:
        query = query.filter(Reserve.user_id == user_id)
    
    # Nếu là mentor, có thể filter theo mentor_id
    if current_user["isMentor"] and mentor_id:
        query = query.filter(Reserve.mentor_id == mentor_id)
    elif current_user["isMentor"]:
        # Mentor chỉ xem reserves của chính mình
        query = query.filter(Reserve.mentor_id == current_user["user"].id)
    
    if status:
        query = query.filter(Reserve.status == status)
    
    reserves = query.all()
    
    # Lấy reserve_details cho từng reserve
    result = []
    for reserve in reserves:
        reserve_dict = {
            "id": reserve.id,
            "user_id": reserve.user_id,
            "mentor_id": reserve.mentor_id,
            "car_id": reserve.car_id,
            "status": reserve.status,
            "createdAt": reserve.createdAt,
            "updatedAt": reserve.updatedAt,
            "reserve_details": []
        }
        
        # Lấy reserve_details
        details = db.query(ReserveDetail).filter(ReserveDetail.reserve_id == reserve.id).all()
        for detail in details:
            reserve_dict["reserve_details"].append({
                "id": detail.id,
                "reserve_id": detail.reserve_id,
                "start_time": detail.start_time,
                "end_time": detail.end_time,
                "price": detail.price,
                "notes": detail.notes,
                "status": detail.status,
                "createdAt": detail.createdAt,
                "updatedAt": detail.updatedAt
            })
        
        result.append(reserve_dict)
    
    return result

@router.get("/{reserve_id}", response_model=ReserveResponse)
def get_reserve(
    reserve_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(currentLoginUser)
):
    """Lấy thông tin reserve theo ID"""
    reserve = db.query(Reserve).filter(Reserve.id == reserve_id).first()
    if not reserve:
        raise HTTPException(status_code=404, detail="Reserve không tồn tại")
    
    # Kiểm tra quyền: user chỉ xem reserves của chính mình, mentor chỉ xem reserves của chính mình
    if not current_user["isMentor"] and reserve.user_id != current_user["user"].id:
        raise HTTPException(status_code=403, detail="Không có quyền truy cập reserve này")
    if current_user["isMentor"] and reserve.mentor_id != current_user["user"].id:
        raise HTTPException(status_code=403, detail="Không có quyền truy cập reserve này")
    
    # Lấy reserve_details
    details = db.query(ReserveDetail).filter(ReserveDetail.reserve_id == reserve.id).all()
    
    reserve_dict = {
        "id": reserve.id,
        "user_id": reserve.user_id,
        "mentor_id": reserve.mentor_id,
        "car_id": reserve.car_id,
        "status": reserve.status,
        "createdAt": reserve.createdAt,
        "updatedAt": reserve.updatedAt,
        "reserve_details": []
    }
    
    for detail in details:
        reserve_dict["reserve_details"].append({
            "id": detail.id,
            "reserve_id": detail.reserve_id,
            "start_time": detail.start_time,
            "end_time": detail.end_time,
            "price": detail.price,
            "notes": detail.notes,
            "status": detail.status,
            "createdAt": detail.createdAt,
            "updatedAt": detail.updatedAt
        })
    
    return reserve_dict

@router.post("/", response_model=ReserveResponse, status_code=status.HTTP_201_CREATED)
def create_reserve(
    reserve: ReserveCreate,
    db: Session = Depends(get_db),
    current_user=Depends(currentLoginUser)
):
    """Đặt lịch hẹn - chỉ user mới có thể đặt lịch"""
    # Chỉ user mới có thể đặt lịch
    if current_user["isMentor"]:
        raise HTTPException(status_code=403, detail="Mentor không thể đặt lịch hẹn")
    
    # Kiểm tra user_id phải là user đang đăng nhập
    if reserve.user_id != current_user["user"].id:
        raise HTTPException(status_code=403, detail="Không thể đặt lịch hẹn cho user khác")
    
    # Kiểm tra user, mentor, car có tồn tại và active không
    user = db.query(User).filter(User.id == reserve.user_id, User.isActive == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại hoặc đã bị vô hiệu hóa")
    
    mentor = db.query(Mentor).filter(Mentor.id == reserve.mentor_id, Mentor.isActive == True).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor không tồn tại hoặc đã bị vô hiệu hóa")
    
    car = db.query(Car).filter(Car.id == reserve.car_id, Car.isActive == True).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car không tồn tại hoặc đã bị vô hiệu hóa")
    
    # Kiểm tra car có available không
    if car.status != "available":
        raise HTTPException(status_code=400, detail="Car không khả dụng")
    
    # Kiểm tra reserve_details không rỗng
    if not reserve.reserve_details or len(reserve.reserve_details) == 0:
        raise HTTPException(status_code=400, detail="Phải có ít nhất một chi tiết đặt lịch")
    
    # Kiểm tra thời gian hợp lệ
    for detail in reserve.reserve_details:
        if detail.end_time <= detail.start_time:
            raise HTTPException(status_code=400, detail="Thời gian kết thúc phải sau thời gian bắt đầu")
        
        # Kiểm tra xung đột thời gian với các reserve khác
        conflicting_reserves = db.query(ReserveDetail).join(
            Reserve, ReserveDetail.reserve_id == Reserve.id
        ).filter(
            Reserve.car_id == reserve.car_id,
            Reserve.status.in_(["pending", "confirmed"]),
            ReserveDetail.start_time < detail.end_time,
            ReserveDetail.end_time > detail.start_time
        ).all()
        
        if conflicting_reserves:
            raise HTTPException(
                status_code=400,
                detail=f"Xe đã được đặt vào khoảng thời gian từ {detail.start_time} đến {detail.end_time}"
            )
    
    # Tạo reserve
    db_reserve = Reserve(
        user_id=reserve.user_id,
        mentor_id=reserve.mentor_id,
        car_id=reserve.car_id,
        status=reserve.status or "pending"  # Sử dụng status từ request hoặc mặc định "pending"
    )
    db.add(db_reserve)
    db.flush()  # Để lấy id của reserve
    
    # Tạo reserve_details
    for detail in reserve.reserve_details:
        # Tính giá tự động nếu không được cung cấp hoặc = 0
        calculated_price = detail.price
        if calculated_price is None or calculated_price == 0:
            # Tính số giờ
            time_diff = detail.end_time - detail.start_time
            hours = time_diff.total_seconds() / 3600.0
            
            # Tính giá = (mentor.price_per_hour + car.price_per_hour) * số giờ
            mentor_price = mentor.price_per_hour or 0
            car_price = car.price_per_hour or 0
            calculated_price = (mentor_price + car_price) * hours
        
        db_detail = ReserveDetail(
            reserve_id=db_reserve.id,
            start_time=detail.start_time,
            end_time=detail.end_time,
            price=calculated_price,
            notes=detail.notes,
            status=detail.status
        )
        db.add(db_detail)
    
    # Cập nhật status của car thành "busy" nếu cần
    # (Có thể để logic này ở đây hoặc tạo một job để cập nhật)
    
    db.commit()
    db.refresh(db_reserve)
    
    # Lấy lại reserve với details để trả về
    details = db.query(ReserveDetail).filter(ReserveDetail.reserve_id == db_reserve.id).all()
    
    reserve_dict = {
        "id": db_reserve.id,
        "user_id": db_reserve.user_id,
        "mentor_id": db_reserve.mentor_id,
        "car_id": db_reserve.car_id,
        "status": db_reserve.status,
        "createdAt": db_reserve.createdAt,
        "updatedAt": db_reserve.updatedAt,
        "reserve_details": []
    }
    
    for detail in details:
        reserve_dict["reserve_details"].append({
            "id": detail.id,
            "reserve_id": detail.reserve_id,
            "start_time": detail.start_time,
            "end_time": detail.end_time,
            "price": detail.price,
            "notes": detail.notes,
            "status": detail.status,
            "createdAt": detail.createdAt,
            "updatedAt": detail.updatedAt
        })
    
    return reserve_dict

