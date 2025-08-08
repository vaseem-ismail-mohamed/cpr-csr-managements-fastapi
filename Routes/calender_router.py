from fastapi import APIRouter, Header
from Controllers.calender_controller import get_events, fetch_students_by_month, update_monthly_status, get_students
from Models.calendar_schema import input, output

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.get("/get-events", response_model=output.GetEvents) #AdminCalender
async def route_get_events(section: str = Header(...)):
    return await get_events(section)

@router.get("/fetchbymonth", response_model=output.FetchStudentsByMonthResponse) #AdminStatusDetails
async def route_fetch_students_by_month(month: str = Header(...), section: str = Header(...)):
    return await fetch_students_by_month(month, section)

@router.post("/update-status", response_model=output.UpdateMonthlyStatus) #AdminStatusDetails
async def route_update_status(data: input.UpdateMonthlyStatus):
    return await update_monthly_status(data)

@router.get("/get-students", response_model=output.GetStudents)
async def route_get_emails(data: input.GetStudents):
    return await get_students(data)