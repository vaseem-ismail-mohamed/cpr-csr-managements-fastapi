from pydantic import BaseModel, EmailStr

class BookSlot(BaseModel):
    section: str
    date: str
    time: str
    email: EmailStr
    student_id: str

class GetBookedSlots(BaseModel):
    section: str
    date: str

class DeleteSlot(BaseModel):
    section: str
    date: str
    time: str

