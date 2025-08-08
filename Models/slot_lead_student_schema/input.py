from pydantic import BaseModel
from typing import Optional

class GetEvents(BaseModel):
    section: str

class BookSlot(BaseModel):
    section: str
    date: str
    admin: str
    student: str
    role: str
    slot: str

class SlotDetails(BaseModel):
    section: str
    date: str

class DeleteSlot(BaseModel):
    section: str
    slot: str
    date: Optional[str]

class GetStudentSlots(BaseModel):
    student_name: str