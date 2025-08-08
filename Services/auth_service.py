from DataBase.db import users_collection
import jwt
from datetime import datetime, timedelta
import bcrypt

secret_key = "CPRFSSAB4CSR"
algorithm = "HS256"

async def create_token(payload: dict, expires_delta: timedelta = None) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def findUserwithemail(email):
    UserFind = await users_collection.find_one({"email": email})
    if UserFind:
        return UserFind
    return None

async def Register(email: str, name: str, password: str, section: str, role: str):
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "name": name,
        "email": email,
        "password": hashed_pass,
        "section": section,
        "role": role
    }
    InsertUser = await users_collection.insert_one(user)
    if InsertUser.inserted_id:
        return InsertUser.inserted_id
    return False

async def findUserwithtoken(email: str):
    Find = await users_collection.find_one({"email": email})
    if (Find):
        return Find
    return None

async def CheckPassword(password: str, hashed_pass: str) -> bool:
    return password == hashed_pass

# async def CheckPassword(password: str, hashed_pass: str) -> bool:
#     # Convert both to bytes before checking
#     return bcrypt.checkpw(password.encode('utf-8'), hashed_pass.encode('utf-8'))

async def UpdateUser(email: str, new_password: str):
    Update = await users_collection.update_one({"email": email}, {"$set":{"password": new_password}})
    if Update:
        return Update
    return None

async def DeleteUser(email: str):
    Delete = await users_collection.delete_one({"email": email})
    if Delete:
        return True
    return False



