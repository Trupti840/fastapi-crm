from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal
from schemas import LeadCreate, LeadResponse
from typing import List
from auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leads")
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    new_lead = models.Lead(**lead.dict())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@router.get("/leads", response_model=List[LeadResponse])
def read_leads(
    status: str = None,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    query = db.query(models.Lead)

    if status:
        query = query.filter(models.Lead.status == status)

    return query.all()