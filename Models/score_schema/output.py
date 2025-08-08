from pydantic import BaseModel

class AddScores(BaseModel):
    message: str

class GetSectionScores(BaseModel):
    scores: list

class GetStudentScores(BaseModel):
    scores: list

class GetScoresByMonth(BaseModel):
    scores: list