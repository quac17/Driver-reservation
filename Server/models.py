from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String, nullable=True)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now()) 


class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    license_number = Column(String(50), nullable=True)
    experience_years = Column(Integer, default=0)
    price_per_hour = Column(Float, default=0)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False, default="question")
    content = Column(String, nullable=False, default="content")
    mark = Column(Float, nullable=False, default=1)
    unit = Column(String(255), nullable=False, default="unit")
    answers = Column(JSONB, nullable=False, default=dict)
    multiple_choice = Column(Boolean, nullable=False, default=False)
    image_url = Column(String(255), nullable=False, default="")
    add_attribute = Column(JSONB, nullable=False, default=dict)
    createdBy = Column(Integer, nullable=False, default=1)
    isDeleted = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now()) 

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False, default="question")
    total_question = Column(Integer, nullable=False, default = 0)
    max_score = Column(Float, nullable=False, default=0)
    total_time = Column(Integer,nullable=False, default=0)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), server_default=func.now())
    createdBy = Column(Integer, nullable=False, default=1)
    isDeleted = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now()) 

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    subject_code = Column(String(255), unique=True, nullable=False, default="0000")
    name = Column(String(255), nullable=False, default="subject")
    isDeleted = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now()) 

class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False, default=0)
    is_finished = Column(Boolean, default=False)
    isDeleted = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)
    isDeleted = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String(20), unique=True, nullable=False)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)
    status = Column(String(20), default='available')
    price_per_hour = Column(Float, default=0)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

class Reserve(Base):
    __tablename__ = "reserves"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    mentor_id = Column(Integer, nullable=False)
    car_id = Column(Integer, nullable=False)
    status = Column(String(20), default='pending')
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

class ReserveDetail(Base):
    __tablename__ = "reserve_details"

    id = Column(Integer, primary_key=True, index=True)
    reserve_id = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    price = Column(Float, default=0)
    notes = Column(String, nullable=True)
    status = Column(String(20), default='pending')
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now()) 

