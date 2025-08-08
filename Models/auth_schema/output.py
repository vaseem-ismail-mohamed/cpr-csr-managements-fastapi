from pydantic import BaseModel

class Login(BaseModel):
    token: str

class Register(BaseModel):
    message: str
    user_id: str
    token: str

class ChangePass(BaseModel):
    message: str

class DeleteUser(BaseModel):
    message: str