from pydantic import BaseModel
from typing import Optional, List

class GetEvents(BaseModel):
    events: list

class FetchStudentsByMonth(BaseModel):
    _id: str
    name: Optional[str] = None
    email: Optional[str] = None
    section: Optional[str] = None
    status: Optional[str] = None

class FetchStudentsByMonthResponse(BaseModel):
    data: list

class UpdateMonthlyStatus(BaseModel):
    modified_count: int

class GetStudents(BaseModel):
    emails: List[str]