# from quart import jsonify, request
from fastapi import HTTPException
from Models.lead_status_schema import input, output
# from pymongo import MongoClient
# from flask_cors import CORS
# from bson.objectid import ObjectId
from DataBase.db import Status_db, users_collection
from Services.calender_service import FindDataBase
from Services.lead_status_service import StudentsList, StatusUpdatetoDB

# app = Flask(__name__)
# CORS(app)

# client = MongoClient("mongodb+srv://vaseemdrive01:mohamedvaseem@cprweb.6sp6c.mongodb.net/")
# student_db = client['CPR-Details'] 
# status_db = client['CPR-Statusers = student_db['Users']


#leads/status.html


# @app.route('/api/students', methods=['GET'])
async def fetch_students(section: str, month: str) -> output.FetchStudents:
    if not section or not month:
        raise HTTPException(status_code=400, detail="Section and month are required")

    students_cursor = await FindDataBase(users_collection, {"section": section, "role": "Student"}, {})
    students = [student async for student in students_cursor]

    month_collection = Status_db[month]
    status_data = {
        str(doc["_id"]): doc.get("status", "Not Complete")
        async for doc in month_collection.find()
    }

    students_list = await StudentsList(students, status_data)
    if not students_list:
        raise HTTPException(status_code=404, detail="Student list is empty")

    return output.FetchStudents(students_list=students_list)

async def update_students_status(data: input.UpdateStudentsStatus) -> input.UpdateStudentsStatus:
    section, month, status_updates = data.section, data.month, data.status_updates
    if not section or not month or not status_updates:
        raise HTTPException(status_code=400, detail="Missing required fields")

    if month not in await Status_db.list_collection_names():
        await Status_db.create_collection(month)

    month_collection = Status_db[month]
    updated = await StatusUpdatetoDB([su.dict() for su in status_updates], month_collection)

    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update status")

    return input.UpdateStudentsStatus(message="Status updated successfully")


# if __name__ == "__main__":
#     app.run