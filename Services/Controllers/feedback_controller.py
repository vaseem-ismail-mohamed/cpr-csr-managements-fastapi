# from flask import Flask, request, jsonify
# from quart import request, jsonify
from fastapi import HTTPException
from Models.feedback_schema import input, output
# from datetime import datetime
# from flask_cors import CORS
# from pymongo import MongoClient
# from datetime import datetime
from Services.feedback_service import InsertSenderReceiver, ValidateDBandGetData
from DataBase.db import Details_db
from Services.calender_service import FindDataBase, users_collection

# app = Flask(__name__)
# CORS(app) 

# # Connect to MongoDB Atlas
# client = MongoClient("mongodb+srv://vaseemdrive01:mohamedvaseem@cprweb.6sp6c.mongodb.net/")
# db = client["CPR-Details"]  
# sectiondb = client['CPR-Details']  
# sections_collection = sectiondb["Users"]

# dis&feed.html
# feedback.html
# dcfb.html


#FeedBack System
# @app.route('/submit-feedback', methods=['POST'])
async def submit_feedback(data: input.SubmitFeedback) -> output.SubmitFeedback:
    success = await InsertSenderReceiver(data.sender, data.reciever, data.feedback)

    if not success:
        raise HTTPException(status_code=400, detail="Insert Failed")

    return output.SubmitFeedback(message=f"Feedback stored in '{data.sender}' and '{data.reciever}' collections")



async def get_feedback_by_email(email: str) -> output.GetFeedback:
    collection_name = email.replace('.', '_').replace('@', '_')
    feedbacks = await ValidateDBandGetData(collection_name)

    if not feedbacks:
        raise HTTPException(status_code=404, detail="No feedback found")

    return output.GetFeedback(feedback=[
        output.FeedbackOut(
            from_=f["from"],
            to=f["to"],
            textcontent=f["textcontent"],
            timestamp=f["timestamp"].isoformat() if hasattr(f["timestamp"], "isoformat") else str(f["timestamp"])
        )
        for f in feedbacks
    ])
    
# # @app.route('/get-feedbacks', methods=['POST'])
# def get_feedbacks():
#     try:
#         data = request.get_json()
#         email = data.get('email')

#         if not email:
#             return jsonify({"error": "Email is required"}), 400

#         # Convert email to collection name format
#         collection_name = email.replace('@', '_').replace('.', '_')
#         if collection_name not in db.list_collection_names():
#             return jsonify({"error": f"No feedbacks found for {email}"}), 404

#         feedback_collection = db[collection_name]
#         feedbacks = list(feedback_collection.find({}, {'_id': 0}))  # Exclude `_id` field
#         return jsonify(feedbacks), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# @app.route('/get-students/<section>', methods=['GET'])
async def get_students(section: str) -> output.GetStudents:
    query = {"section": section}
    projection = {"_id": 0, "email": 1}
    cursor = await FindDataBase(users_collection, query, projection)

    emails = [student["email"] async for student in cursor]
    if not emails:
        raise HTTPException(status_code=404, detail=f"No students found in section {section}")

    return output.GetStudents(emails=emails)
    

# # @app.route('/get-feedback/<email>', methods=['GET'])
# async def get_feedback_by_email(request, email: str):
#     """
#     Fetch feedback for a given student's email.
#     """
#     try:
#         # Sanitize the email to get the collection name
#         collection_name = email.replace('.', '_').replace('@', '_')

#         # Check if the collection exists
#         if collection_name not in Details_db.list_collection_names():
#             return jsonify({"error": f"No feedback found for {email}"}), 404

#         # Retrieve feedback documents from the collection
#         # feedback_collection = Details_db[collection_name]
#         # feedbacks = list(feedback_collection.find({}, {"_id": 0}))
#         feedbacks = await list(FindDataBase(Details_db[collection_name], {}, {"_id": 0}))
#         if not feedbacks:
#             return jsonify({"error": "Feedbacks not Found"}), 400

#         return jsonify({"feedbacks": feedbacks}), 200
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return jsonify({"error": str(e)}), 500
    
    
# if __name__ == "__main__":
#     app.run(debug=True)
