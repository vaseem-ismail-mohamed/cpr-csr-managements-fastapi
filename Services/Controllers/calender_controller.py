from fastapi import HTTPException
from Models.calendar_schema import input, output
from DataBase.db import users_collection, Status_db
from Services.calender_service import section_exists, serialize_event, FindEvents, serialize_student, Update_Data, FindDataBase

# SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP provider
# SMTP_PORT = 587
# EMAIL_SENDER = "cpr.bot.ai@gmail.com"
# EMAIL_PASSWORD = "hahk mply jiez tgja"  # Use environment variables for security

# SectionA = ["canvas9787839798@gmail.com", "canvas9787839798@gmail.com"]
# SectionB = ["canvas9787839798@gmail.com", "canvas9787839798@gmail.com"]
# SectionC = ["mohamed.ismail@fssa.freshworks.com", "canvas9787839798@gmail.com"]


# bookcpr.html


async def get_events(section: str) -> output.GetEvents:
    try:
        if not await section_exists(section):
            raise HTTPException(status_code=404, detail=f"Section '{section}' not found")

        events = await FindEvents(section)
        print("Events :", events)
        # print("Serialize Event :", serialize_event(event) for event in events)
        return output.GetEvents(events=[await serialize_event(event) for event in events])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def fetch_students_by_month(month: str, section: str) -> output.FetchStudentsByMonthResponse:
    print("Month :", month, "Section :", section)
    try:
        if section:
            cursor = Status_db[month].find({"section": section}).sort("name", 1)
        else:
            cursor = Status_db[month].find().sort("_id", 1)

        students = await cursor.to_list(length=None)
        return output.FetchStudentsByMonthResponse(data=[await serialize_student(student) for student in students])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




async def update_monthly_status(data: input.UpdateMonthlyStatus) -> output.UpdateMonthlyStatus:
    try:
        result = await Update_Data(data.student_id, data.new_status, data.month)
        return {"modified_count": result.modified_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_students(data: input.GetStudents) -> output.GetStudents:
    section = data.section
    try:
        query1 = {"section": section}
        query2 = {"_id": 0, "email": 1}
        cursor = await FindDataBase(users_collection, query1, query2)

        emails = [student["email"] async for student in cursor]
        if not emails:
            raise HTTPException(status_code=404, detail=f"No students found in section {section}")

        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.route('/get-feedback/<email>', methods=['GET'])
# def get_feedback_by_email(email):
#     """
#     Fetch feedback for a given student's email.
#     """
#     try:
#         # Sanitize the email to get the collection name
#         collection_name = email.replace('.', '_').replace('@', '_')

#         # Check if the collection exists
#         if collection_name not in sectiondb.list_collection_names():
#             return jsonify({"error": f"No feedback found for {email}"}), 404

#         # Retrieve feedback documents from the collection
#         feedback_collection = sectiondb[collection_name]
#         feedbacks = list(feedback_collection.find({}, {"_id": 0}))

#         return jsonify({"feedbacks": feedbacks}), 200
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return jsonify({"error": str(e)}), 500
    
# @app.route('/add-goals', methods=['POST'])
# def add_multiple_goals():
#     """
#     Admin adds a single message containing goals for multiple subjects for a specific student.
#     """
#     data = request.json
#     print(data)
#     section = data.get('section')
#     student_name = data.get('to')
#     admin_name = data.get('from', 'Admin')  # Default sender is Admin
#     goals = data.get('goals', [])  # List of goals for subjects
#     month = data.get('month', datetime.now().strftime("%Y-%m"))  # Use selected month or default to current
    

#     if not section or not student_name or not goals:
#         return jsonify({"error": "Section, student name, and goals are required"}), 400

#     collection_name = f"track_goals_{section}"
#     collection = track_db[collection_name]

#     message = {
#         "from": admin_name,
#         "to": student_name,
#         "month": month,
#         "goals": goals,  # Store all subject goals in one entry
#     }

#     collection.insert_one(message)

#     return jsonify({"message": "Goals added successfully"}), 201



# @app.route('/student-goals', methods=['GET'])
# def get_student_goals():
#     """
#     Fetch all goals for a specific student by name, section, and month.
#     """
#     student_name = request.args.get('name')
#     section = request.args.get('section')
#     month = request.args.get('month')  # Get the selected month

#     if not student_name or not section or not month:
#         return jsonify({"error": "Student name, section, and month are required"}), 400

#     collection_name = f"track_goals_{section}"
#     collection = track_db[collection_name]

#     goals = collection.find(
#         {"to": student_name, "month": month},
#         {"_id": 0, "from": 1, "to": 1, "goals": 1}
#     )

#     return jsonify({"goals": list(goals)})






# if __name__ == '__main__':
#     app.run(debug=True)
