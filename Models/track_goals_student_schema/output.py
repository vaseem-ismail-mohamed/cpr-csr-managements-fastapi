from pydantic import BaseModel

class GoalEntry(BaseModel):
    from_: str
    to: str
    goals: list

class GetStudentGoals(BaseModel):
    goals: list