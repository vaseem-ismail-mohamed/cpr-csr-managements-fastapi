# from quart import jsonify, request
from fastapi import HTTPException
from Models.meet_student_schema import input, output
from datetime import datetime, timedelta
# from flask_cors import CORS
# from pymongo import MongoClient
# import smtplib
# from email.mime.text import MIMEText
from DataBase.db import bookings_collection
from Services.meet_student_service import generate_default_slots, generate_slots, send_email, UpdateCollection, GetAdminEmails
# from Services.calender_service import FindDataBase


# app = Flask(__name__)
# CORS(app)



# MongoDB Configuration
# client = MongoClient("mongodb+srv://vaseemdrive01:mohamedvaseem@cprweb.6sp6c.mongodb.net/")
# db = client["student_booking"] 
# bookings_collection = db["bookings"] 

# SectionA = ["madasamimadasami2002@gmail.com", "canvas9787839798@gmail.com"]
# SectionB = ["madasamy.asokan@fssa.freshworks.com", "canvas9787839798@gmail.com"]
# SectionC = ["mohamed.ismail@fssa.freshworks.com", "canvas9787839798@gmail.com"]

# # SMTP Configuration
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# EMAIL_SENDER = "cpr.bot.ai@gmail.com"
# EMAIL_PASSWORD = "blty ihcf xbwg ocgb" 


# meet-student.html



# def generate_default_slots():
#     """Generate default time slots between 2 PM and 5 PM (6 slots, 30 minutes each)."""
#     start_time = datetime.strptime("14:00", "%H:%M")
#     end_time = datetime.strptime("17:00", "%H:%M")
#     slots = []
#     while start_time < end_time:
#         slots.append({
#             "time": start_time.strftime("%H:%M"),
#             "booked": False,
#             "student_id": None,
#         })
#         start_time += timedelta(minutes=30)
#     return slots



# def generate_slots(date):
#     """Generate time slots between 2 PM and 5 PM (6 slots, 30 minutes each)."""
#     base_time = datetime.strptime(f"{date} 14:00", "%Y-%m-%d %H:%M")
#     return [
#         {"time": (base_time + timedelta(minutes=30 * i)).strftime("%H:%M"), "booked": False}
#         for i in range(6)
#     ]
    




async def get_slots(section: str, date: str) -> output.GetSlots:
    print("Section :", section, "Date :", date)
    slot_doc = await bookings_collection.find_one({"section": section, "date": date})

    if not slot_doc:
        default_slots = await generate_slots(date)
        slot_doc = {
            "section": section,
            "date": date,
            "slots": default_slots
        }
        await bookings_collection.insert_one(slot_doc)

    return output.GetSlots(slots=slot_doc["slots"])


async def get_calendar(section: str) -> output.GetCalendar:
    today = datetime.today()
    start_of_month = today.replace(day=1)
    end_of_month = (
        start_of_month.replace(month=today.month + 1, day=1) - timedelta(days=1)
        if today.month < 12
        else start_of_month.replace(month=1, year=today.year + 1) - timedelta(days=1)
    )

    calendar = []
    current_day = start_of_month

    while current_day <= end_of_month:
        date_str = current_day.strftime("%Y-%m-%d")
        slot_doc = await bookings_collection.find_one({"section": section, "date": date_str})

        if not slot_doc:
            default_slots = await generate_default_slots()
            new_slot_doc = {
                "section": section,
                "date": date_str,
                "slots": default_slots
            }
            await bookings_collection.insert_one(new_slot_doc)
            slot_doc = new_slot_doc

        fully_booked = all(slot["booked"] for slot in slot_doc["slots"])
        calendar.append({
            "date": date_str,
            "fully_booked": fully_booked
        })

        current_day += timedelta(days=1)

    return output.GetCalendar(calender=calendar)


async def book_slot(data: input.BookSlot) -> output.BookSlot:
    section = data.section
    date = data.date
    time = data.time
    email = data.email
    student_id = data.student_id

    result = await UpdateCollection(section, date, time, email, student_id)

    if not result:
        raise HTTPException(status_code=400, detail="Slot not available or already booked.")

    admin_emails = await GetAdminEmails(section)

    await send_email(
        to_emails=admin_emails,
        subject="New Booking Confirmation",
        message=f"Student {student_id} has booked a slot.\nDate: {date}\nTime: {time}\nSection: {section}"
    )

    await send_email(
        to_emails=[student_id],
        subject="Booking Confirmed",
        message=f"Dear {student_id},\nYour slot is confirmed on {date} at {time}.\nSection: {section}"
    )

    updated_doc = await bookings_collection.find_one({"section": section, "date": date})
    return output.BookSlot(
        message="Slot successfully booked!",
        slots=updated_doc["slots"]
    )


# if __name__ == "__main__":
#     app.run(debug=True)