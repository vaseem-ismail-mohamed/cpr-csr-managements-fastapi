from fastapi import HTTPException
from Models.ai_schema import input, output
from Services.ai_service import decode_token, BasicResponse
from datetime import datetime

async def Handle_Ai_Response(token: str, data: input.AiInput) -> output.AiOutput:
    text_input = data.input
    name = data.name
    token_decode = await decode_token(token)
    #print("Token Decode :", token_decode)
    role = token_decode.get("role", "Admin")

    Handle_Basic_Response = await BasicResponse(text_input, role, name)
    # if not Handle_Basic_Response:
    #     print("Input :", text_input, "Date :", date, "Time :", time, "Problem :", "while response generation", "Role :", role )
    #     raise HTTPException(status_code=404, detail="Unable to generate response sorry for the server error, we will fix soon, thank you!!!")
    
    return output.AiOutput(message=str(Handle_Basic_Response), links=[])
