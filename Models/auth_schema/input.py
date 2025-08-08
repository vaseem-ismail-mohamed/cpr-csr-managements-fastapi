from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str

class Register(BaseModel):
    name: str
    email: str
    password: str
    section: str
    role: str

class ChangePass(BaseModel):
    email: str
    current_password: str
    new_password: str

class DeleteUser(BaseModel):
    email: str