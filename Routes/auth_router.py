from fastapi import APIRouter
from Models.auth_schema import input,output
from Controllers.auth_controller import register, change_password, login, delete_user

router = APIRouter(prefix='/auth', tags=["Auth"])


@router.post('/register', response_model=output.Register)
async def HandleRegister(data: input.Register):
    return await register(data)

@router.post("/change-password", response_model=output.ChangePass)
async def handle_change_password(data: input.ChangePass):
    return await change_password(data)

@router.post("/login", response_model=output.Login)
async def handle_login(data: input.Login):
    return await login(data)

@router.delete("/delete-user", response_model=output.DeleteUser)
async def handle_delete_user(data: input.DeleteUser):
    return await delete_user(data)
