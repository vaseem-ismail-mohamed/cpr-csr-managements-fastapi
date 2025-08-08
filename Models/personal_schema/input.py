from pydantic import BaseModel, EmailStr

class GetAdminNotes(BaseModel):
    name: str
    email: EmailStr
    Title: str
    Notes: str
    date: str

class AllAdminNotes(BaseModel):
    name: str

class GetLeadNotes(BaseModel):
    name: str
    email: EmailStr
    topic: str
    Notes: str
    date: str
    

class AllLeadNotes(BaseModel):
    name: str