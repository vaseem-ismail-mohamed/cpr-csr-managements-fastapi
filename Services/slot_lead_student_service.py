from DataBase.db import calenderdb
from email.mime.text import MIMEText
from datetime import datetime
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "cpr.bot.ai@gmail.com"
EMAIL_PASSWORD = "hahk mply jiez tgja"

SectionA = ["canvas9787839798@gmail.com", "canvas9787839798@gmail.com"]
SectionB = ["canvas9787839798@gmail.com", "canvas9787839798@gmail.com"]
SectionC = ["mohamed.ismail@fssa.freshworks.com", "canvas9787839798@gmail.com"]


# ✅ Check if collection exists
async def section_exists(section: str) -> bool:
    collections = await calenderdb.list_collection_names()
    return section in collections


# ✅ Get collection object
async def get_collection(section: str):
    return calenderdb[section]


# ✅ Get all events for section
async def get_events_database(section: str):
    collection = await get_collection(section)
    cursor = collection.find()
    return await cursor.to_list(length=None)


# ✅ Send email
async def send_email(to_emails: list, subject: str, message: str):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(to_emails)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_emails, msg.as_string())

        print(f"✅ Email sent to: {to_emails}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# ✅ Serialize MongoDB event (ObjectId -> str)
async def serialize_event(event: dict):
    event["_id"] = str(event["_id"])
    if "start_time" in event:
        event["start_time"] = event["start_time"].isoformat()
    if "end_time" in event:
        event["end_time"] = event["end_time"].isoformat()
    return event


# ✅ Insert slot into section/student collection
async def InsertDataToCollection(event_data: dict, section: str) -> bool:
    collection = await get_collection(section)
    result = await collection.insert_one(event_data)
    return result.acknowledged


# ✅ Get admin emails by section
async def getAdminEmails(section: str):
    if section == "A":
        return SectionA
    elif section == "B":
        return SectionB
    elif section == "C":
        return SectionC
    return []


# ✅ Find slot by custom query
async def FindDatasbyQuery(query: dict, projection: dict, section: str):
    collection = await get_collection(section)
    return await collection.find_one(query, projection)


# ✅ Delete slot by query
async def DeleteSlotBySection(query: dict, section: str) -> bool:
    collection = await get_collection(section)
    result = await collection.delete_one(query)
    print('result :', result)
    return result.acknowledged
