from fastapi import APIRouter
from Controllers.cpr_admin_controller import update_Monthly_status
from Models.cpr_admin_schema import input, output

router = APIRouter(prefix="/admin", tags=["CPR-Admin"])

@router.post("/update-status", response_model=output.UpdateMonthlyStatus)
async def route_update_student_status(data: input.UpdateMonthlyStatus):
    return await update_Monthly_status(data)
