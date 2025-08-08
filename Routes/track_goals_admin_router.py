from fastapi import APIRouter
from Models.track_goals_admin_schema import input, output
from Controllers.track_goals_admin_controller import add_multiple_goals

router = APIRouter(prefix="/admin/goals", tags=["Admin Goals"])

@router.post("/add", response_model=output.AddMultipleGoals) #GoalsAdminTrack
async def route_add_goals(data: input.AddMultipleGoals):
    return await add_multiple_goals(data)