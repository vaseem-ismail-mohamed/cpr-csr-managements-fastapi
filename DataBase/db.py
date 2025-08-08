# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://vaseemdrive01:mohamedvaseem@cprweb.6sp6c.mongodb.net/"  # Replace with your MongoDB Atlas connection string
# mongo_client = MongoClient(MONGO_URI)
mongo_client = AsyncIOMotorClient(MONGO_URI)

#DataBase
Details_db = mongo_client['CPR-Details']
calenderdb = mongo_client["Slot-Book"]
Status_db = mongo_client['CPR-Status']
score_db = mongo_client["Scores"]
track_db = mongo_client["track_goals"]
booking_db = mongo_client["student_booking"] 
notes_admin_db = mongo_client["Notes-admin"]
notes_lead_db = mongo_client["Notes-lead"]
ai_module_db = mongo_client["ai-admin-student"]

#Collections
users_collection = Details_db['Users']
bookings_collection = booking_db["bookings"]
ai_sreekala_collection = ai_module_db["admin-ai-sreekala"]
ai_mohamed_collection = ai_module_db["student-ai-mohamed"]
ai_response_collection = ai_module_db["ai-modules-response"]
