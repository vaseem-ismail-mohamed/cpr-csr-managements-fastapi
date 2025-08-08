from DataBase.db import track_db

async def InsertGoalsinCollection(collection_name: str, message: dict) -> bool:
    collection = track_db[collection_name]
    if collection is None:
        return None
    result = await collection.insert_one(message)
    return bool(result.inserted_id)
