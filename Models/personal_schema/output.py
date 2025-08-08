from pydantic import BaseModel

class GetAdminNotes(BaseModel):
    message: str

class AllAdminNotes(BaseModel):
    data: list

class GetLeadNotes(BaseModel):
    message: str

class AllLeadNotes(BaseModel):
    data: list