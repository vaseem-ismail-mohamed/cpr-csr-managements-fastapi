from pydantic import BaseModel, EmailStr
from typing import List

class SubmitFeedback(BaseModel):
    message: str

class FeedbackOut(BaseModel):
    from_: EmailStr
    to: EmailStr
    textcontent: str
    timestamp: str

class GetFeedback(BaseModel):
    feedback: List[FeedbackOut]

class GetStudents(BaseModel):
    emails: List[EmailStr]