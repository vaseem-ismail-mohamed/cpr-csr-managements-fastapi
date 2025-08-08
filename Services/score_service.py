import datetime
from DataBase.db import score_db


async def Current_Month():
    return datetime.datetime.utcnow().strftime("%B")


async def CreateDynamicCollection(section: str):
    return score_db[f"scoredb{section}"]


async def UpdateStudentData(email: str, scores: list, section: str, month: str):
    current_month = datetime.datetime.utcnow().strftime("%B")
    collection = score_db[f"Section_{section}"]
    student_data = {
        "email": email,
        "month": month,
        "scores": scores,
        "timestamp": datetime.datetime.utcnow()
    }
    
    FindExists = await collection.find_one({"email": email}, {})
    if not FindExists:
        result = await collection.insert_one(student_data)
        if not result:
            return None
        return result.inserted_id
    else:
        result = await collection.update_one(
            {"email": email, "month": current_month},
            {"$set": student_data},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None


async def FindScores(query: dict, section: str):
    collection = score_db[f"Section_{section}"]
    print("Collection :", collection)
    cursor = collection.find(query, {"_id": 0})
    print("Data :", cursor)
    return await cursor.to_list(length=None)
