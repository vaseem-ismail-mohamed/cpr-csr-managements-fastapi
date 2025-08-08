from fastapi import APIRouter, Header, Body
from Models.ai_schema import input, output
from Controllers.ai_controller import Handle_Ai_Response


router = APIRouter(prefix="/ai/response", tags=["AIResponse"])

@router.post('/admin-ai-response', response_model=output.AiOutput)
async def route_response_for_sreekala(token: str = Header(...), data: input.AiInput = Body(...)):
    return await Handle_Ai_Response(token, data)