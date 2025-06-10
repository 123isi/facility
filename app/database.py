from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from sqlalchemy.exc import OperationalError

# 데이터베이스 연결 URL을 환경 변수에서 가져오거나 기본값을 사용합니다
# 기본값: MySQL 데이터베이스에 대한 연결 정보
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@db:3306/facility_db")


def get_engine():
    """
    데이터베이스 엔진을 생성하고 연결을 테스트하는 함수
    연결 실패 시 최대 5번까지 재시도합니다
    """
    max_retries = 5  # 최대 재시도 횟수
    retry_interval = 5  # 재시도 간격(초)

    for attempt in range(max_retries):
        try:
            # SQLAlchemy 엔진 생성
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            # 연결 테스트를 위한 간단한 쿼리 실행
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            return engine
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise e
            print(f"데이터베이스 연결 실패. {retry_interval}초 후 재시도...")
            time.sleep(retry_interval)


# 데이터베이스 엔진 생성
engine = get_engine()

# 데이터베이스 세션 생성기 설정
# autocommit=False: 자동 커밋 비활성화
# autoflush=False: 자동 플러시 비활성화
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델의 기본 클래스 생성
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션을 생성하고 관리하는 제너레이터 함수
    세션 사용이 완료되면 자동으로 닫힙니다
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()