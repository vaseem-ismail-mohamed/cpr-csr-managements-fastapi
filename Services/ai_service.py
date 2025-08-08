from DataBase.db import ai_mohamed_collection, ai_sreekala_collection, users_collection
from Services.response_service import correct_input_with_symspell
import jwt
from Services.response_service import generate_response
from datetime import datetime

secret_key = "CPRFSSAB4CSR"
algorithm = "HS256"

async def decode_token(token: str) -> dict:
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    #print("payload :", payload)
    return payload


async def BasicResponse(input: str, role: str, name: str) -> any:
    now = datetime.now()
    date = now.date()
    time = now.time()

    # Step 1: Auto-correct user input
    corrected_input = correct_input_with_symspell(input)

    # handling_dynamic_response = await get_dynamic_response(corrected_input)
    # response = str(handling_dynamic_response) if handling_dynamic_response else "I'm not sure how to respond."
    
    inp, out = generate_response(input)
    response = out

    # Step 3: Store original + corrected input in MongoDB
    log_entry = {
        "original-input": input,
        "corrected-input": corrected_input,
        "ai-response": response,
        "role": role,
        "date": str(date),
        "time": str(time)
    }

    if role == "Admin":
        await ai_sreekala_collection.insert_one(log_entry)
    else:
        await ai_mohamed_collection.insert_one(log_entry)

    return response
