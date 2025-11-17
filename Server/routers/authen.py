import os
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import get_db
from models import User, Mentor

load_dotenv()
router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

invalidated_tokens = set()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authen/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # Thêm jti (JWT ID) để có thể invalidate token
    to_encode.update({"jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        jti: str = payload.get("jti")
        
        if username is None or jti is None:
            raise credentials_exception
            
        # Kiểm tra token có bị invalidate không
        if jti in invalidated_tokens:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    return username

def currentLoginUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Hàm kiểm tra và trả về thông tin user hoặc mentor hiện tại đang đăng nhập
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        jti: str = payload.get("jti")
        user_type: str = payload.get("type", "user")  # user hoặc mentor
        
        if username is None or jti is None:
            raise credentials_exception
            
        # Kiểm tra token có bị invalidate không
        if jti in invalidated_tokens:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Tìm user hoặc mentor trong database
    if user_type == "mentor":
        mentor = db.query(Mentor).filter(Mentor.username == username).first()
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor không tồn tại")
        if not mentor.isActive:
            raise HTTPException(status_code=403, detail="Mentor đã bị vô hiệu hóa")
        return {"user": mentor, "isMentor": True}
    else:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User không tồn tại")
        if not user.isActive:
            raise HTTPException(status_code=403, detail="User đã bị vô hiệu hóa")
        return {"user": user, "isMentor": False}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Đăng nhập cho cả User và Mentor
    """
    # Thử tìm mentor trước
    mentor = db.query(Mentor).filter(Mentor.username == form_data.username).first()
    user = None
    
    loginUser = None
    isMentor = False
    user_type = "user"
    
    if mentor:
        if not mentor.isActive:
            raise HTTPException(status_code=403, detail="Tài khoản mentor đã bị vô hiệu hóa")
        if mentor.password != form_data.password:
            raise HTTPException(status_code=400, detail="Sai tên đăng nhập hoặc mật khẩu")
        loginUser = mentor
        isMentor = True
        user_type = "mentor"
    else:
        # Nếu không phải mentor, tìm user
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user:
            raise HTTPException(status_code=400, detail="Sai tên đăng nhập hoặc mật khẩu")
        if not user.isActive:
            raise HTTPException(status_code=403, detail="Tài khoản user đã bị vô hiệu hóa")
        if user.password != form_data.password:
            raise HTTPException(status_code=400, detail="Sai tên đăng nhập hoặc mật khẩu")
        loginUser = user
        isMentor = False
        user_type = "user"
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": loginUser.username, "type": user_type}, expires_delta=access_token_expires
    )
    
    login_data = {
        "username": loginUser.username,
        "name": loginUser.name,
        "isMentor": isMentor
    }
    
    # Thêm thông tin riêng cho mentor
    if isMentor:
        login_data["license_number"] = mentor.license_number
        login_data["experience_years"] = mentor.experience_years
    else:
        login_data["email"] = user.email
        login_data["phone"] = user.phone
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "message": {
            "loginData": login_data
        } 
    }

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    try:
        # Decode token để lấy jti
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti: str = payload.get("jti")
        
        if jti:
            # Thêm jti vào invalidated_tokens để invalidate token
            invalidated_tokens.add(jti)
            
        return {"msg": "Logout thành công. Token đã được invalidate."}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")

@router.post("/reset-token")
def reset_token(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")
    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_type: str = payload.get("type", "user")
        if username is None:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")
    
    # Tìm user hoặc mentor
    if user_type == "mentor":
        mentor = db.query(Mentor).filter(Mentor.username == username).first()
        if not mentor:
            raise HTTPException(status_code=404, detail="Mentor không tồn tại")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": mentor.username, "type": "mentor"}, expires_delta=access_token_expires
        )
    else:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User không tồn tại")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "type": "user"}, expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"} 