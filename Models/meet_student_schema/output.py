from pydantic import BaseModel

class GetSlots(BaseModel):
    slots: list

class GetCalendar(BaseModel):
    calender: list

class BookSlot(BaseModel):
    message: str
    slots: list
    