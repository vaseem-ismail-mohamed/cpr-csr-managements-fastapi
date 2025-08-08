from pydantic import BaseModel, EmailStr
from typing import List

class StudentOut(BaseModel):
    name: str
    email: EmailStr
    status: str
    
class FetchStudents(BaseModel):
    students_list: List[StudentOut]

class UpdateStudentStatus(BaseModel):
    message: str