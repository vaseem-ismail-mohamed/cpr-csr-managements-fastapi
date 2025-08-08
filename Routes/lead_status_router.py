from fastapi import APIRouter, Header
from Controllers.lead_status_controller import fetch_students, update_students_status
from Models.lead_status_schema import input, output

router = APIRouter(prefix="/lead-status", tags=["Lead Status"])

@router.get("/get-students", response_model=output.FetchStudents) #LeadCprStatus
async def get_students(section: str = Header(...), month: str = Header(...)):
    return await fetch_students(section, month)

@router.post("/update-status", response_model=output.UpdateStudentStatus)
async def update_status(data: input.UpdateStudentsStatus):
    return await update_students_status(data)