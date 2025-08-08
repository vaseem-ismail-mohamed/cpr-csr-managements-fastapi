from fastapi import APIRouter, Header, Query
from Models.slot_lead_student_schema import input, output
from Controllers.slot_lead_student_controller import get_events, book_slot, slot_details, delete_slot, get_student_slots

router = APIRouter(prefix="/slot-lead", tags=["Slot Lead"])

@router.get("/get-events", response_model=output.GetEvents)
async def Route_Get_Events(section: str = Header(...)):
    return await get_events(section)

@router.delete("/delete-slot", response_model=output.DeleteSlot) #AdminCalender #LeadCalendar
async def Route_Delete__Slot(data: input.DeleteSlot):
    return await delete_slot(data)

@router.post('/book-slot', response_model=output.BookSlot)  #AdminCalender
async def Route_Book__Slot(data: input.BookSlot):
    return await book_slot(data)

@router.get("/slot-details", response_model=output.SlotDetails)
async def Route_Slot_Details(data: input.SlotDetails):
    return await slot_details(data)

@router.get('/student-slots', response_model=output.GetStudentSlots) #StudentCprRequest
async def Route_Get_Student_Slots(student_name: str = Query(...)):
    return await get_student_slots(student_name)