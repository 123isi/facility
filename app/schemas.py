from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import FacilityType

# 시설 관련 스키마 정의
class FacilityBase(BaseModel):
    """
    시설 정보의 기본 스키마
    모든 시설 관련 스키마의 기본이 되는 클래스입니다
    """
    name: str  # 시설 이름
    type: FacilityType  # 시설 유형 (스포츠, 도서관, 커뮤니티 센터)
    location: str  # 시설 위치
    capacity: Optional[int] = None  # 수용 인원 (선택적)
    description: Optional[str] = None  # 시설 설명 (선택적)

class FacilityCreate(FacilityBase):
    """
    시설 생성 시 사용되는 스키마
    FacilityBase를 상속받아 추가 필드 없이 사용
    """
    pass

class FacilityUpdate(FacilityBase):
    """
    시설 정보 업데이트 시 사용되는 스키마
    모든 필드가 선택적으로 변경 가능
    """
    name: Optional[str] = None
    type: Optional[FacilityType] = None
    location: Optional[str] = None

class Facility(FacilityBase):
    """
    시설 정보 조회 시 사용되는 스키마
    데이터베이스에서 조회된 시설 정보를 포함
    """
    id: int  # 시설 ID
    created_at: datetime  # 생성 시간
    updated_at: datetime  # 수정 시간

    class Config:
        orm_mode = True  # ORM 모드 활성화

# 예약 관련 스키마 정의
class ReservationBase(BaseModel):
    """
    예약 정보의 기본 스키마
    모든 예약 관련 스키마의 기본이 되는 클래스입니다
    """
    facility_id: int  # 예약할 시설 ID
    user_name: str  # 예약자 이름
    user_phone: str  # 예약자 전화번호
    start_time: datetime  # 예약 시작 시간
    end_time: datetime  # 예약 종료 시간
    purpose: Optional[str] = None  # 예약 목적 (선택적)
    capacity: int  # 예약 인원

class ReservationCreate(ReservationBase):
    """
    예약 생성 시 사용되는 스키마
    ReservationBase를 상속받아 추가 필드 없이 사용
    """
    pass

class ReservationUpdate(ReservationBase):
    """
    예약 정보 업데이트 시 사용되는 스키마
    모든 필드가 선택적으로 변경 가능
    """
    facility_id: Optional[int] = None
    user_name: Optional[str] = None
    user_phone: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class Reservation(ReservationBase):
    """
    예약 정보 조회 시 사용되는 스키마
    데이터베이스에서 조회된 예약 정보를 포함
    """
    id: int  # 예약 ID
    created_at: datetime  # 생성 시간
    updated_at: datetime  # 수정 시간

    class Config:
        orm_mode = True