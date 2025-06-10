from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List,Optional

from app import schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"]
)

# templates 디렉터리 경로 (app/templates)
templates = Jinja2Templates(directory="app/templates")


# ───────────────────────────────────────────────────────────────────────────────
# 1) HTML 목록 페이지
# ───────────────────────────────────────────────────────────────────────────────
@router.get("/")
def list_facilities(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    facilities = db.query(models.Facility).offset(skip).limit(limit).all()
    return templates.TemplateResponse(
        "facilities/list.html",
        {"request": request, "facilities": facilities}
    )


# ───────────────────────────────────────────────────────────────────────────────
# 2) HTML 등록 폼
# ───────────────────────────────────────────────────────────────────────────────
@router.get("/new")
def new_facility_form(request: Request):
    # FacilityType enum 클래스 자체를 넘겨서 <select> 옵션으로 사용
    return templates.TemplateResponse(
        "facilities/new.html",
        {"request": request, "types": models.FacilityType}
    )


@router.post("/new")
def create_facility_form(
    request: Request,
    name: str       = Form(...),
    type: str       = Form(...),
    location: str   = Form(...),
    capacity: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    db: Session     = Depends(get_db),
):
    obj = models.Facility(
        name=name,
        type=models.FacilityType(type),
        location=location,
        capacity=capacity,
        description=description,
    )
    db.add(obj)
    db.commit()
    # 등록 후 목록 페이지로 리다이렉트
    return RedirectResponse(url="/facilities/", status_code=303)


# ───────────────────────────────────────────────────────────────────────────────
# 3) JSON CRUD API
# ───────────────────────────────────────────────────────────────────────────────
@router.post("/", response_model=schemas.Facility)
def create_facility_api(
    facility: schemas.FacilityCreate,
    db: Session = Depends(get_db)
):
    db_facility = models.Facility(**facility.dict())
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility


@router.get("/{facility_id}", response_model=schemas.Facility)
def get_facility_api(
    facility_id: int,
    db: Session = Depends(get_db)
):
    facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility


@router.put("/{facility_id}", response_model=schemas.Facility)
def update_facility_api(
    facility_id: int,
    facility: schemas.FacilityUpdate,
    db: Session = Depends(get_db)
):
    db_facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
    if not db_facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    for key, val in facility.dict(exclude_unset=True).items():
        setattr(db_facility, key, val)

    db.commit()
    db.refresh(db_facility)
    return db_facility


@router.delete("/{facility_id}")
def delete_facility_api(
    facility_id: int,
    db: Session = Depends(get_db)
):
    facility = db.query(models.Facility).filter(models.Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    db.delete(facility)
    db.commit()
    return {"message": "Facility deleted successfully"}
