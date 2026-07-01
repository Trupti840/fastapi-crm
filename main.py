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
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import Form
from fastapi.responses import RedirectResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")

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

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
    name="login.html",
    context={"request": request}
)

@app.post("/login-ui")
def login_ui(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.email == email).first()

    if not db_user or not verify_password(password, db_user.password):
        return {"error": "Invalid credentials"}

    token = create_access_token({"sub": db_user.email})

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="token", value=token)

    return response

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    leads = db.query(models.Lead).all()
    statues = ["new", "contacted", "qualified", "lost", "won"]
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "leads": leads,
        "statues": statues
    })

@app.get("/create-lead", response_class=HTMLResponse)
def create_lead_page(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(models.User).all()  # ✅ fetch users
    statues = ["new", "contacted", "qualified", "lost", "won"]  # ✅ define statuses

    return templates.TemplateResponse(
        "create_lead.html",
        {
            "request": request,
            "users": users,   # ✅ pass to template
            "statues": statues  # ✅ pass to template
        }
    )

@app.post("/create-lead-ui")
def create_lead_ui(
    name: str = Form(...),
    email: str = Form(...),
    status: str = Form(None),
    owner_id: int = Form(...),
    db: Session = Depends(get_db)
):
    new_lead = models.Lead(name=name, email=email, status=status, owner_id=owner_id)
    db.add(new_lead)
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=302)

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        return {"error": "Invalid email"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid password"}

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token}

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("token")
    return response

Base.metadata.create_all(bind=engine)
