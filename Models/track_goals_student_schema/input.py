from pydantic import BaseModel

class GetStudentGoals(BaseModel):
    name: str
    section: str
    month: str