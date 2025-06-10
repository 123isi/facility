from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime

# 시설 유형을 정의하는 열거형 클래스
class FacilityType(enum.Enum):
    SPORTS = "sports"  # 스포츠 시설
    LIBRARY = "library"  # 도서관
    COMMUNITY_CENTER = "community_center"  # 커뮤니티 센터

# 시설 정보를 저장하는 데이터베이스 모델
class Facility(Base):
    __tablename__ = "facilities"  # 데이터베이스 테이블 이름

    # 기본 키 및 인덱스
    id = Column(Integer, primary_key=True, index=True)
    # 시설 이름 (최대 100자)
    name = Column(String(100), nullable=False)
    # 시설 유형 (FacilityType 열거형 사용)
    type = Column(Enum(FacilityType), nullable=False)
    # 시설 위치 (최대 200자)
    location = Column(String(200), nullable=False)
    # 수용 인원
    capacity = Column(Integer)
    # 시설 설명 (최대 500자)
    description = Column(String(500))
    # 생성 시간 (자동 설정)
    created_at = Column(DateTime, default=datetime.utcnow)
    # 수정 시간 (자동 업데이트)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Reservation 모델과의 관계 설정 (1:N)
    reservations = relationship("Reservation", back_populates="facility")

# 예약 정보를 저장하는 데이터베이스 모델
class Reservation(Base):
    __tablename__ = "reservations"  # 데이터베이스 테이블 이름

    # 기본 키 및 인덱스
    id = Column(Integer, primary_key=True, index=True)
    # 예약된 시설의 외래 키
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    # 예약자 이름 (최대 100자)
    user_name = Column(String(100), nullable=False)
    # 예약자 전화번호 (최대 20자)
    user_phone = Column(String(20), nullable=False)
    # 예약 시작 시간
    start_time = Column(DateTime, nullable=False)
    # 예약 종료 시간
    end_time = Column(DateTime, nullable=False)
    # 예약 목적 (최대 200자)
    purpose = Column(String(200))
    # 예약 인원
    capacity = Column(Integer)
    # 생성 시간 (자동 설정)
    created_at = Column(DateTime, default=datetime.utcnow)
    # 수정 시간 (자동 업데이트)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Facility 모델과의 관계 설정 (N:1)
    facility = relationship("Facility", back_populates="reservations")