from fastapi import APIRouter, Header
from Models.feedback_schema import input, output
from Controllers.feedback_controller import submit_feedback, get_feedback_by_email, get_students

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/submit", response_model=output.SubmitFeedback) #AdminFeedback
async def route_submit_feedback(data: input.SubmitFeedback):
    return await submit_feedback(data)

@router.get("/get-feedbacks", response_model=output.GetFeedback) #AdminFeedback #LeadFeedBack
async def route_get_feedbacks(email: str = Header(...)):
    return await get_feedback_by_email(email)

@router.get("/get-students", response_model=output.GetStudents) #LeadFeedBack
async def route_get_students_by_section(section : str = Header(...)):
    return await get_students(section)