from DataBase.db import track_db

async def FindStudentGoals(collection_name: str, student_name: str, month: str):
    collection = track_db[collection_name]
    if collection is None:
        return None
    cursor = collection.find(
        {"to": student_name, "month": month},
        {"_id": 0, "from": 1, "to": 1, "goals": 1}
    )
    return await cursor.to_list(length=None)
