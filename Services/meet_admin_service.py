import datetime
from email.mime.text import MIMEText
import smtplib
from DataBase.db import booking_db, bookings_collection

SectionA = ["madasamimadasami2002@gmail.com", "canvas9787839798@gmail.com"]
SectionB = ["madasamy.asokan@fssa.freshworks.com", "canvas9787839798@gmail.com"]
SectionC = ["mohamed.ismail@fssa.freshworks.com", "canvas9787839798@gmail.com"]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "cpr.bot.ai@gmail.com"
EMAIL_PASSWORD = "blty ihcf xbwg ocgb"

async def format_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")

async def send_email(to_emails, subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(to_emails)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_emails, msg.as_string())
        print(f"Email sent to {to_emails}")
    except Exception as e:
        print(f"Failed to send email: {e}")

async def BookOnDB(section, date, time, email, student_id):
    result = await bookings_collection.update_one(
        {"section": section, "date": date, "slots.time": time, "slots.booked": False},
        {"$set": {
            "slots.$.booked": True,
            "booked-email": email,
            "slots.$.student_id": student_id
        }}
    )
    return result.modified_count > 0

async def AssignAdminEmails(section: str):
    if section == "A": return SectionA
    if section == "B": return SectionB
    if section == "C": return SectionC
    return []

async def GetBookedSlots(slot_cursor):
    booked_slots = []
    docs = await slot_cursor.to_list(length=None)  # Convert cursor to a list of docs

    for doc in docs:
        for slot in doc.get("slots", []):
            if slot.get("booked"):
                booked_slots.append({
                    "time": slot.get("time"),
                    "student_id": slot.get("student_id")
                })

    return booked_slots


async def UpdateSlotFalse(section, date, time):
    result = await bookings_collection.update_one(
        {"section": section, "date": date, "slots.time": time, "slots.booked": True},
        {"$set": {"slots.$.booked": False, "slots.$.student_id": None}}
    )
    return result.modified_count > 0
