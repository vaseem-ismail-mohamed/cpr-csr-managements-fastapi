from pydantic import BaseModel, EmailStr
from typing import Optional

class AddScores(BaseModel):
    section: str
    month: str
    email: EmailStr
    scores: list

class GetSectionScores(BaseModel):
    section: str
    month: str

class GetStudentScores(BaseModel):
    email: EmailStr
    section: str
    month: str

class GetScoresByMonth(BaseModel):
    section: str
    month: str