from pydantic import BaseModel
from typing import List

class BookSlot(BaseModel):
    message: str
    slots: List[dict]
    
class GetBookedSlots(BaseModel):
    booked_slots: List[dict]

class DeleteSlot(BaseModel):
    message: str