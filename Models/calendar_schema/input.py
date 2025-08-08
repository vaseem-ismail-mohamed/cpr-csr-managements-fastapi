from pydantic import BaseModel

class GetEvents(BaseModel):
    section: str

class FetchStudentsByMonth(BaseModel):
    month: str
    section: str

class UpdateMonthlyStatus(BaseModel):
    month: str
    student_id: str
    new_status: str

class GetStudents(BaseModel):
    section: str