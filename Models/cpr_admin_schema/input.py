from pydantic import BaseModel

class UpdateMonthlyStatus(BaseModel):
    student_id: str
    status: str
    month: str