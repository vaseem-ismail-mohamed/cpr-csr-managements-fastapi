from datetime import datetime
from fastapi import HTTPException
from Models.track_goals_admin_schema import input, output
from Services.track_goals_admin_service import InsertGoalsinCollection

async def add_multiple_goals(data: input.AddMultipleGoals) -> output.AddMultipleGoals:
    section = data.section
    student_name = data.to
    admin_name = data.from_ or "Admin"
    goals = data.goals
    month = data.month or datetime.now().strftime("%Y-%m")

    if not section or not student_name or not goals:
        raise HTTPException(status_code=400, detail="Section, student name, and goals are required.")

    collection_name = f"track_goals_{section}"

    message = {
        "from": admin_name,
        "to": student_name,
        "month": month,
        "goals": [goal.dict() for goal in goals],
    }

    result = await InsertGoalsinCollection(collection_name, message)
    if not result:
        raise HTTPException(status_code=404, detail="Insertion in database failed")

    return output.AddMultipleGoals(message="Goals added successfully")
