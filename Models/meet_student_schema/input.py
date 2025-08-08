from pydantic import BaseModel, EmailStr

class GetSlots(BaseModel):
    section: str
    date: str

class GetCalendar(BaseModel):
    section: str
    date: str

class BookSlot(BaseModel):
    section: str
    date: str
    time: str
    email: EmailStr
    student_id: str