from fastapi import HTTPException, status
from Services.auth_service import findUserwithemail, Register, findUserwithtoken, UpdateUser, DeleteUser, create_token, CheckPassword
from Models.auth_schema import input, output

# from DataBase.db import users_collection
# from pymongo import MongoClient
# from flask_cors import CORS
# from datetime import datetime
# import re
# import jwt

# # Flask app setup
# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes and origins

# # Security configurations
# bcrypt = Bcrypt(app)
# app.config['JWT_SECRET_KEY'] = '460680e7fe09d19e4063e23c51d3c53757920b054007273cd083703623c1cfea'  # Replace with your secret key
# jwt = JWTManager(app)





# login.html
# register.html
# change.html
# delete-user.html





async def register(data: input.Register) -> output.Register:
    if not all([data.name, data.email, data.password, data.section, data.role]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required")

    existing_user = await findUserwithemail(data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user_id = await Register(data.email, data.name, data.password, data.section, data.role)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Insert Failed")
    
    token_payload = {
        'name': data.name,
        'email': data.email,
        'password': data.password,
        'section': data.section,
        'role': data.role
    }
    
    token = await create_token(token_payload)

    return output.Register(message="User registered successfully", user_id=str(user_id), token=token)


async def change_password(data: input.ChangePass) -> output.Login:
    if not all([data.email, data.current_password, data.new_password]):
        raise HTTPException(status_code=400, detail="All fields are required")

    user = await findUserwithtoken(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user['password'] != data.current_password:
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    await UpdateUser(data.email, data.new_password)
    return {"message": "Password updated successfully"}


async def login(data: input.Login) -> output.Login:
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = await findUserwithemail(data.email)
    if not user:
        raise HTTPException( status_code=404, detail="User Not Found")
    PasswordCheck = await CheckPassword(data.password, user['password'])
    if not PasswordCheck:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return output.Login(token=user['token'])
    

async def delete_user(data: input.DeleteUser) -> output.DeleteUser:
    user = await findUserwithemail(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await DeleteUser(data.email)
    return output.DeleteUser(message="User deleted successfully")