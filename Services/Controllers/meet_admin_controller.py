# from quart import jsonify, request
from fastapi import HTTPException
from Models.meet_admin_schema import input, output
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# from flask_cors import CORS
# import smtplib
# from email.mime.text import MIMEText
from DataBase.db import bookings_collection
from Services.calender_service import FindDataBase
from Services.meet_admin_service import format_date, send_email, BookOnDB, AssignAdminEmails, GetBookedSlots, UpdateSlotFalse

# app = Flask(__name__)
# CORS(app)

# meet-admin.html

# # MongoDB Configuration
# client = MongoClient("mongodb+srv://vaseemdrive01:mohamedvaseem@cprweb.6sp6c.mongodb.net/")
# db = client["student_booking"]  # Database name
# bookings_collection = db["bookings"]  # Collection for storing bookings

# SectionA = ["madasamimadasami2002@gmail.com", "canvas9787839798@gmail.com"]
# SectionB = ["madasamy.asokan@fssa.freshworks.com", "canvas9787839798@gmail.com"]
# SectionC = ["mohamed.ismail@fssa.freshworks.com", "canvas9787839798@gmail.com"]

# # SMTP Configuration
# SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP provider
# SMTP_PORT = 587
# EMAIL_SENDER = "cpr.bot.ai@gmail.com"
# EMAIL_PASSWORD = "blty ihcf xbwg ocgb"  # Use environment variables for security



# meet-admin.html









# def send_email(to_emails, subject, message):
#     """Send an email notification."""
#     try:
#         msg = MIMEText(message)
#         msg["Subject"] = subject
#         msg["From"] = EMAIL_SENDER
#         msg["To"] = ", ".join(to_emails)

#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#             server.sendmail(EMAIL_SENDER, to_emails, msg.as_string())
#         print(f"Email sent to {to_emails}")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

async def book_slot(data: input.BookSlot) -> output.BookSlot:
    section, date, time, email, student_id = data.section, data.date, data.time, data.email, data.student_id

    if not all([section, date, time, student_id]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    result = await BookOnDB(section, date, time, email, student_id)

    if result:
        admin_emails = await AssignAdminEmails(section)

        subject_admin = "New Booking Confirmation"
        message_admin = f"Student {student_id} has booked a slot.\nDate: {date}\nTime: {time}\nSection: {section}"

        subject_student = "Booking Confirmed"
        message_student = f"Dear {student_id},\nYour slot is confirmed on {date} at {time}.\nSection: {section}"

        await send_email(admin_emails, subject_admin, message_admin)
        await send_email([student_id], subject_student, message_student)

        updated_slot_doc = await bookings_collection.find_one({"section": section, "date": date})

        if not updated_slot_doc:
            raise HTTPException(status_code=404, detail="Data not Found")

        return output.BookSlot(
            message="Slot successfully booked!",
            slots=updated_slot_doc.get("slots", [])
        )

    raise HTTPException(status_code=400, detail="Slot not available or already booked.")

async def get_booked_slots(section: str, date: str) -> output.GetBookedSlots:
    slot_doc = await FindDataBase(bookings_collection, {"section": section, "date": date}, {})
    if not slot_doc:
        raise HTTPException(status_code=404, detail="No slots found for the given section and date.")

    booked_slots = await GetBookedSlots(slot_doc)
    return output.GetBookedSlots(booked_slots=booked_slots or [])

async def delete_slot(data: input.DeleteSlot) -> output.DeleteSlot:
    section = data.section
    date = await format_date(data.date)
    time = data.time

    if not all([section, date, time]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    result = await UpdateSlotFalse(section, date, time)

    if result:
        return output.DeleteSlot(message="Slot Deleted Successfully!")

    raise HTTPException(status_code=400, detail="Failed to delete slot. It might not be booked.")


# def format_date(date_str):
#     return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")



# if __name__ == "__main__":
#     app.run(debug=True)
