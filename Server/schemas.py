from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime
from typing import List

class UserBase(BaseModel):
    username: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
    isActive: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    isActive: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class MentorBase(BaseModel):
    username: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    experience_years: Optional[int] = 0
    price_per_hour: Optional[float] = 0

class MentorCreate(MentorBase):
    password: str

class MentorUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    experience_years: Optional[int] = None
    price_per_hour: Optional[float] = None
    password: Optional[str] = None
    isActive: Optional[bool] = None

class MentorResponse(MentorBase):
    id: int
    isActive: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    message: Dict[str, Any]

# Question
class QuestionBase(BaseModel):
    subject_id: Optional[int] = None
    title: str = "question"
    content: str = "content"
    mark: float = 1.0
    unit: str = "unit"
    answers: Dict[str, Any] = Field(default_factory=dict)
    multiple_choice: bool = False
    image_url: str = ""
    add_attribute: Dict[str, Any] = Field(default_factory=dict)
    createdBy: Optional[int] = None
    isDeleted: Optional[bool] = False
    isActive: Optional[bool] = True

    class Config:
        from_attributes = True

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    subject_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    mark: Optional[float] = None
    unit: Optional[str] = None
    answers: Optional[Dict[str, Any]] = None
    multiple_choice: Optional[bool] = None
    image_url: Optional[str] = None
    add_attribute: Optional[Dict[str, Any]] = None
    createdBy: Optional[int] = None
    isDeleted: Optional[bool] = None
    isActive: Optional[bool] = None

class QuestionResponse(QuestionBase):
    id: int
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

    class Config:
        from_attributes = True

# Exam
class ExamBase(BaseModel):
    subject_id: Optional[int] = None
    title: str = "question"
    total_question: int = 0
    total_time: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    createdBy: Optional[int] = None
    isDeleted: Optional[bool] = False

    class Config:
        from_attributes = True

class ExamCreate(ExamBase):
    subject_id: int
    createdBy: int
    total_questions: int
    total_time: int
    mark: float

class ExamResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    total_question: int
    max_score: float
    total_time: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    createdBy: int
    isDeleted: Optional[bool] = False
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class ExamListResponse(BaseModel):
    data: List[ExamResponse] 
    class Config:
        from_attributes = True

class Question(BaseModel):
    question_id: int
    content: str
    answer: List[str]
    multi_choice: bool
    img: str

class QuestionWithAnswer(BaseModel):
    question_id: int
    content: str
    answer: List[str]
    img: str
    correct_answer: int

class submitAnswer(BaseModel):
    question_id: int
    answer: List[int]

class ExamSubmitForm(BaseModel):
    list_answer: List[submitAnswer]

# Car
class CarBase(BaseModel):
    license_plate: str
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    status: Optional[str] = "available"
    price_per_hour: Optional[float] = 0

class CarResponse(CarBase):
    id: int
    isActive: bool
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

# Reserve
class ReserveDetailBase(BaseModel):
    start_time: datetime
    end_time: datetime
    price: Optional[float] = 0
    notes: Optional[str] = None
    status: Optional[str] = "pending"

class ReserveDetailCreate(ReserveDetailBase):
    pass

class ReserveDetailResponse(ReserveDetailBase):
    id: int
    reserve_id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReserveBase(BaseModel):
    user_id: int
    mentor_id: int
    car_id: int
    status: Optional[str] = "pending"

class ReserveCreate(BaseModel):
    user_id: int
    mentor_id: int
    car_id: int
    status: Optional[str] = "pending"
    reserve_details: List[ReserveDetailCreate]

class ReserveResponse(ReserveBase):
    id: int
    reserve_details: List[ReserveDetailResponse] = []
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
