from datetime import datetime, timezone
from DataBase.db import notes_admin_db, notes_lead_db


async def GetDate() -> str:
    return datetime.now(timezone.utc).date().isoformat()


async def GetTime() -> str:
    return datetime.now(timezone.utc).time().strftime("%H:%M:%S")


async def GetNotesAdminCollName(name: str):
    return notes_admin_db[name]


async def InsertAdminColl(name: str, date: str, time: str, email: str, Title: str, Notes: str) -> bool:
    notes_admin_collection = await GetNotesAdminCollName(name)
    result = await notes_admin_collection.insert_one({
        "name": name,
        "date": date,
        "time": time,
        "email": email,
        "Title": Title,
        "Notes": Notes
    })
    return bool(result.inserted_id)


async def FindAdminColl(name: str):
    notes_admin_collection = await GetNotesAdminCollName(name)
    return notes_admin_collection.find({}, {"_id": 0})


async def GetNotesLeadCollName(name: str):
    return notes_lead_db[name]


async def InsertLeadColl(name: str, date: str, time: str, email: str, Title: str, Notes: str) -> bool:
    notes_lead_collection = await GetNotesLeadCollName(name)
    result = await notes_lead_collection.insert_one({
        "name": name,
        "date": date,
        "time": time,
        "email": email,
        "Notes": Notes,
        "Title": Title
    })
    return bool(result.inserted_id)


async def FindLeadColl(name: str):
    notes_lead_collection = await GetNotesLeadCollName(name)
    return notes_lead_collection.find({}, {"_id": 0})
