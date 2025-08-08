from fastapi import APIRouter, Header, Query
from Models.meet_student_schema import input, output
from Controllers.meet_student_controller import get_slots, get_calendar, book_slot

router = APIRouter(prefix="/student", tags=["Meet Student"])

@router.get("/slots", response_model=output.GetSlots) #AdminSlotBook
async def route_get_slots(section: str = Header(...), date: str = Query(...)):
    return await get_slots(section, date)

@router.get("/calendar", response_model=output.GetCalendar) #AdminSlotBook
async def route_get_calendar(section: str = Header(...)):
    return await get_calendar(section)

@router.post("/book-slot", response_model=output.BookSlot)
async def route_book_slot(data: input.BookSlot):
    return await book_slot(data)