from fastapi import APIRouter
from Controllers.lead_overall_controller import get_lead_overall_statistics
from Models.lead_overall_schema import input, output

router = APIRouter(prefix="/lead" , tags=["Lead Overall Stats"])

@router.post('/overall/details', response_model=output.GetLeadOverallStatistics)
async def route_get_lead_overall(data: input.GetLeadOverallStatistics):
    return await get_lead_overall_statistics(data)