from pydantic import BaseModel, EmailStr

class SubmitFeedback(BaseModel):
    sender: EmailStr
    reciever: EmailStr
    feedback: str

class GetFeedback(BaseModel):
    email: EmailStr

class GetStudents(BaseModel):
    section: str