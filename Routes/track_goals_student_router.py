from fastapi import APIRouter, Header
from Models.track_goals_student_schema import input, output
from Controllers.track_goals_student_controller import get_student_goals

router = APIRouter(prefix="/student/goals", tags=["Student Goals"])

@router.get("/get", response_model=output.GetStudentGoals)
async def router_get_student_goals(name: str = Header(...), section: str = Header(...), month: str = Header(...)):
    return await get_student_goals(name, section, month)
