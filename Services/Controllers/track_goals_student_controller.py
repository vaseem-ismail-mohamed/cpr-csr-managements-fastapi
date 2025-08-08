from fastapi import HTTPException
from Models.track_goals_student_schema import input, output
from Services.track_goals_student_service import FindStudentGoals

async def get_student_goals(name: str, section: str, month: str) -> output.GetStudentGoals:
    student_name = name

    if not student_name or not section or not month:
        raise HTTPException(status_code=400, detail="Student name, section, and month are required.")

    collection_name = f"track_goals_{section}"

    result = await FindStudentGoals(collection_name, student_name, month)
    if not result:
        raise HTTPException(status_code=404, detail="Goals not found for student.")

    return output.GetStudentGoals(goals=result)
