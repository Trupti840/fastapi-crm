from pydantic import BaseModel

class LeadCreate(BaseModel):
    name: str
    email: str

class LeadUpdate(BaseModel):
    name: str
    email: str
    status: str
    owner_id: int

class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    status: str
    owner_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str