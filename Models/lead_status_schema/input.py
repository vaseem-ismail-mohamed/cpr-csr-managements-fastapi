from pydantic import BaseModel
from typing import List

class FetchStudents(BaseModel):
    section: str
    month: str
    
class StudentStatusUpdate(BaseModel):
    student_id: str
    status: str

class UpdateStudentsStatus(BaseModel):
    section: str
    month: str
    status_updates: List[StudentStatusUpdate]


