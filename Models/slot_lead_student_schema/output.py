from pydantic import BaseModel
from typing import List

class GetEvents(BaseModel):
    events: List[dict]

class BookSlot(BaseModel):
    message: str

class SlotDetails(BaseModel):
    slot: dict

class DeleteSlot(BaseModel):
    message: str

class GetStudentSlots(BaseModel):
    slots: List[dict]