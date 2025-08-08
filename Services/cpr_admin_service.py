from bson import ObjectId
from DataBase.db import Status_db


async def serialize_student(student: dict) -> dict:
    student['_id'] = str(student['_id'])
    return student


async def get_collection(month: str):
    return Status_db[month]


async def UpdateDetails(month: str, query: dict, update: dict) -> bool:
    collection = await get_collection(month)
    if collection is None:
        return False

    result = await collection.update_one(query, {"$set": update})
    return result.modified_count > 0
