from fastapi import APIRouter, Header, Query
from Models.personal_schema import input, output
from Controllers.personal_controller import post_admin_notes, post_lead_notes, all_admin_notes, all_lead_notes

router = APIRouter(prefix="/personal-notes", tags=["Personal"])

@router.post("/post-notes-admin",response_model=output.GetAdminNotes) #AdminPrivateNotes
async def Get_Admin_Notes(data: input.GetAdminNotes):
    return await post_admin_notes(data)
    
@router.get("/get-all-notes-admin",response_model=output.AllAdminNotes) #AdminNotesShow
async def All_Admin_Notes(name: str = Query(...)):
    return await all_admin_notes( name )
    
@router.post("/post-notes-lead",response_model=output.GetLeadNotes)
async def Get_Lead_Notes(data: input.GetLeadNotes):
    return await post_lead_notes(data)
    
@router.get("/get-all-notes-lead",response_model=output.AllLeadNotes)
async def All_Lead_Notes(name: str = Query(...)):
    return await all_lead_notes(name)