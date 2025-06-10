from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import engine, SessionLocal, get_db
from app import models
from app.routers import facilities, reservations
from sqlalchemy.orm import Session

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(title="공공시설 예약 시스템")

# 애플리케이션 시작 시 데이터베이스 테이블 자동 생성
models.Base.metadata.create_all(bind=engine)

# Jinja2 템플릿 엔진 설정
# HTML 템플릿 파일은 app/templates 디렉토리에 위치
templates = Jinja2Templates(directory="app/templates")

# 정적 파일(CSS, JavaScript, 이미지 등) 설정
# 정적 파일은 app/static 디렉토리에 위치
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 기능별 라우터 등록
app.include_router(facilities.router)  # 시설 관련 라우터
app.include_router(reservations.router)  # 예약 관련 라우터

def init_db(db: Session):
    """
    데이터베이스 초기화 함수
    시설 데이터가 없는 경우 기본 데이터를 추가합니다
    """
    # 시설 데이터 존재 여부 확인
    facilities = db.query(models.Facility).first()
    if not facilities:
        # 기본 시설 데이터 정의
        default_facilities = [
            models.Facility(
                name="종합체육관",
                type=models.FacilityType.SPORTS,
                location="서울시 강남구 테헤란로 123",
                capacity=100,
                description="다목적 체육시설로 농구장, 배구장, 배드민턴장이 구비되어 있습니다."
            ),
            models.Facility(
                name="중앙도서관",
                type=models.FacilityType.LIBRARY,
                location="서울시 서초구 서초대로 456",
                capacity=200,
                description="3층 규모의 종합 도서관으로 열람실, 세미나실이 구비되어 있습니다."
            ),
            models.Facility(
                name="주민센터",
                type=models.FacilityType.COMMUNITY_CENTER,
                location="서울시 송파구 올림픽로 789",
                capacity=50,
                description="다목적 강당과 회의실이 구비된 주민센터입니다."
            )
        ]
        # 기본 데이터를 데이터베이스에 추가
        db.add_all(default_facilities)
        db.commit()
        print("기본 시설 데이터가 추가되었습니다.")

@app.on_event("startup")
async def startup_event():
    """
    애플리케이션 시작 시 실행되는 이벤트 핸들러
    데이터베이스 초기화를 수행합니다
    """
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    """
    메인 페이지 라우트 핸들러
    모든 시설 정보를 조회하여 메인 페이지를 렌더링합니다
    """
    # 모든 시설 정보 조회
    facilities = db.query(models.Facility).all()
    # index.html 템플릿을 사용하여 응답 생성
    return templates.TemplateResponse("index.html", {
        "request": request,
        "facilities": facilities
    })