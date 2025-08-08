from fastapi import APIRouter, Header, Query
from Models.meet_admin_schema import input, output
from Controllers.meet_admin_controller import get_booked_slots,delete_slot, book_slot

router = APIRouter(prefix="/meet-admin", tags=["Meet Admin"])

@router.post("/book-slot", response_model=output.BookSlot)
async def route_book_slot(data: input.BookSlot):
    return await book_slot(data)

@router.get("/booked-slots", response_model=output.GetBookedSlots) #AdminSlotBook
async def router_get_booked_slots(section: str = Header(...), date: str = Query(...)):
    return await get_booked_slots(section, date)

@router.delete("/delete-slot", response_model=output.DeleteSlot)
async def router_delete_slot(data: input.DeleteSlot):
    return await delete_slot(data)