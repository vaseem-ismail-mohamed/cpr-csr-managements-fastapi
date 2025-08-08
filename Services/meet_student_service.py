from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib
from DataBase.db import bookings_collection


# Admin emails per section
SectionA = ["madasamimadasami2002@gmail.com", "canvas9787839798@gmail.com"]
SectionB = ["madasamy.asokan@fssa.freshworks.com", "canvas9787839798@gmail.com"]
SectionC = ["mohamed.ismail@fssa.freshworks.com", "canvas9787839798@gmail.com"]

# SMTP Configuration (Tip: Move to .env for security)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "cpr.bot.ai@gmail.com"
EMAIL_PASSWORD = "blty ihcf xbwg ocgb"


async def generate_default_slots():
    """Generate default time slots between 2 PM and 5 PM (6 slots, 30 minutes each)."""
    start_time = datetime.strptime("14:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    slots = []
    while start_time < end_time:
        slots.append({
            "time": start_time.strftime("%H:%M"),
            "booked": False,
            "student_id": None
        })
        start_time += timedelta(minutes=30)
    return slots


async def generate_slots(date: str):
    """Generate slots for a specific date between 2 PM and 5 PM."""
    base_time = datetime.strptime(f"{date} 14:00", "%Y-%m-%d %H:%M")
    return [
        {"time": (base_time + timedelta(minutes=30 * i)).strftime("%H:%M"), "booked": False}
        for i in range(6)
    ]


async def GetAdminEmails(section: str):
    """Return admin email list based on section."""
    section_map = {
        "A": SectionA,
        "B": SectionB,
        "C": SectionC
    }
    return section_map.get(section, [])


async def send_email(to_emails: list, subject: str, message: str):
    """Send an email using SMTP."""
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(to_emails)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_emails, msg.as_string())

        print(f"✅ Email sent to {to_emails}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")


async def UpdateCollection(section: str, date: str, time: str, email: str, student_id: str) -> bool:
    """Update the booking collection to mark a slot as booked."""
    result = await bookings_collection.update_one(
        {"section": section, "date": date, "slots.time": time, "slots.booked": False},
        {
            "$set": {
                "slots.$.booked": True,
                "booked-email": email,
                "slots.$.student_id": student_id
            }
        }
    )
    return result.modified_count > 0
