from DataBase.db import bookings_collection, calenderdb, Status_db, users_collection
from bson import ObjectId


# Serialize a calendar event (convert ObjectId & datetime to string)
async def serialize_event(event: dict) -> dict:
    event["_id"] = str(event["_id"])
    if "start_time" in event and hasattr(event["start_time"], "isoformat"):
        event["start_time"] = event["start_time"].isoformat()
    if "end_time" in event and hasattr(event["end_time"], "isoformat"):
        event["end_time"] = event["end_time"].isoformat()
    return event


# Check if the section (collection) exists in the calendar DB
async def section_exists(section: str) -> bool:
    collections = await calenderdb.list_collection_names()
    return section in collections


# Get student records for a section & month
async def Find_by_Section(section: str, month: str):
    collection = Status_db[month]
    query = {"section": section} if section else {}
    sort_field = "name" if section else "_id"
    cursor = collection.find(query).sort(sort_field, 1)
    students = await cursor.to_list(length=None)
    return students


# Get calendar events from a section
async def FindEvents(section: str):
    events_collection = calenderdb[section]
    cursor = events_collection.find()
    events = await cursor.to_list(length=None)
    return events


# Serialize a student record (convert _id to string)
async def serialize_student(student: dict) -> dict:
    student["_id"] = str(student["_id"])
    return student


# Update a student's status in a given month
async def Update_Data(student_id: str, new_status: str, month: str):
    result = await Status_db[month].update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"status": new_status}}
    )
    return result


# Generic database find operation with projection
async def FindDataBase(coll, query: dict, projection: dict):
    cursor = coll.find(query, projection)
    print("Cursor :", cursor)
    return cursor
