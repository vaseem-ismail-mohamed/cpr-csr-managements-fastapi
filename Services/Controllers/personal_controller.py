from fastapi import HTTPException
from Models.personal_schema import input, output
from Services.personal_service import GetDate, GetTime, InsertAdminColl, FindAdminColl, InsertLeadColl, FindLeadColl


async def post_admin_notes(data: input.GetAdminNotes) -> output.GetAdminNotes:
    Title = data.Title
    Notes = data.Notes
    email = data.email
    name = data.name

    if not email or not Notes or not Title:
        raise HTTPException(status_code=400, detail="Missing required fields: email, Title or Notes")

    date = data.date
    time = await GetTime()

    result = await InsertAdminColl(name, date, time, email, Title, Notes)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to insert note into admin database")

    return output.GetAdminNotes(message="The data has been saved successfully")


async def all_admin_notes(name: str) -> output.AllAdminNotes:
    print("Name :", name)
    notes = await FindAdminColl(name)
    notes_list = await notes.to_list(length=None) if notes else []

    if not notes_list:
        raise HTTPException(status_code=404, detail="No admin notes found")

    return output.AllAdminNotes(data=notes_list)


async def post_lead_notes(data: input.GetLeadNotes) -> output.GetLeadNotes:
    topic = data.topic
    Notes = data.Notes
    email = data.email

    if not email or not Notes or not topic:
        raise HTTPException(status_code=400, detail="Missing required fields: email, Title or Notes")

    date = data.date or await GetDate()
    time = await GetTime()

    result = await InsertLeadColl(data.name, date, time, email, topic, Notes)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to insert note into lead database")

    return output.GetLeadNotes(message="The data has been saved successfully")


async def all_lead_notes(name: str) -> output.AllLeadNotes:
    notes = await FindLeadColl(name)
    notes_list = await notes.to_list(length=None) if notes else []

    if not notes_list:
        raise HTTPException(status_code=404, detail="No lead notes found")

    return output.AllLeadNotes(data=notes_list)
