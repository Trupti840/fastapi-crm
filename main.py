from fastapi import FastAPI
from database import engine, Base
import models
from database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
from auth import hash_password, verify_password, create_access_token
from schemas import LeadCreate, LeadUpdate, LeadResponse, UserCreate, UserLogin
from auth import get_current_user


app = FastAPI()
@app.get("/")
def home():
    return {"message": "CRM is running!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/leads")
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    new_lead = models.Lead(
    name=lead.name,
    email=lead.email,
    owner_id=user.id
)
    # import pdb; pdb.set_trace() used this to debug and check the values of new_lead and user.id
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return {"message": f"Lead created by {user}", "lead": new_lead}

@app.get("/leads")
def read_leads(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return db.query(models.Lead).all()

@app.put("/leads/{lead_id}")
def update_lead(lead_id: int, lead_data: LeadUpdate, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()

    if not lead:
        return {"error": "Lead not found"}

    for key, value in lead_data.dict().items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)
    return lead

@app.get("/leads/{lead_id}", response_model=LeadResponse)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead:
        return lead
    return {"error": "Lead not found"}

@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead:
        db.delete(lead)
        db.commit()
        return {"message": "Lead deleted"}
    return {"error": "Lead not found"}

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        return {"error": "Email already registered"}
    new_user = models.User(
        email=user.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        return {"error": "Invalid email"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid password"}

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token}

Base.metadata.create_all(bind=engine)
