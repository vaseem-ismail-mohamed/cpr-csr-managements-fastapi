from fastapi import HTTPException
from Models.slot_lead_student_schema import input, output
from Services.slot_lead_student_service import section_exists, get_events_database, send_email, serialize_event, InsertDataToCollection, getAdminEmails, FindDatasbyQuery, DeleteSlotBySection

# app = Flask(__name__)

# # Enable CORS for all routes
# CORS(app)

# # MongoDB connection
# client = MongoClient("mongodb+srv://vaseemdrive01:mohamedvaseem@cprweb.6sp6c.mongodb.net/")
# calenderdb = client["Slot-Book"]
# db = client['CPR-Status']
# scoredb = client["Scores"]
# invitedb = client['Slot_Booking']
# sectiondb = client['CPR-Details']  
# sections_collection = sectiondb["Users"]
# track_db = client["track_goals"]
# student_db = client['CPR-Details'] 
# status_db = client['CPR-Status'] 
# students_collection = student_db['Users']  

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# EMAIL_SENDER = "cpr.bot.ai@gmail.com"
# EMAIL_PASSWORD = "hahk mply jiez tgja"

# SectionA = ["canvas9787839798@gmail.com", "canvas9787839798@gmail.com"]
# SectionB = ["canvas9787839798@gmail.com", "canvas9787839798@gmail.com"]
# SectionC = ["mohamed.ismail@fssa.freshworks.com", "canvas9787839798@gmail.com"]

# showslot.html
# get-req.html

# Helper to serialize MongoDB ObjectId




# Get events for a specific section

async def get_events(section: str) -> output.GetEvents:
    if not await section_exists(section):
        raise HTTPException(status_code=404, detail=f"Section '{section}' not found")

    events = await get_events_database(section)
    if not events:
        return output.GetEvents(events=[])
    
    serialized = [await serialize_event(event) for event in events]
    return output.GetEvents(events=serialized)


async def book_slot(data: input.BookSlot) -> output.BookSlot:
    time = data.slot.replace("AM", "")
    event_data = {
        "date": data.date,
        "admin": data.admin,
        "student": data.student,
        "role": data.role,
        "slot": data.slot,
        "section": data.section,
    }

    admin_emails = await getAdminEmails(data.section)
    if not admin_emails:
        raise HTTPException(status_code=400, detail="Admin emails not found")

    await send_email(
        [data.student],
        "CPR Slot Booking Details - Admin",
        f"Your Coach {data.admin} has booked a slot with {data.student}.\nDate: {data.date}\nSection: {data.section}"
    )

    await send_email(
        admin_emails,
        "Booking Confirmed - CPR - AI",
        f"Dear {admin_emails} your CPR Booking with {data.student} is Booked and the email sent to {data.student}"
    )

    inserted = await InsertDataToCollection(event_data, data.section)
    if not inserted:
        raise HTTPException(status_code=400, detail="Failed to insert slot")

    student_key = data.student.replace(" ", "_")
    inserted_student = await InsertDataToCollection(event_data, student_key)
    if not inserted_student:
        raise HTTPException(status_code=400, detail="Failed to insert into student collection")

    return output.BookSlot(message="Slot booked successfully")


async def slot_details(data: input.SlotDetails) -> output.SlotDetails:
    if not await section_exists(data.section):
        raise HTTPException(status_code=404, detail=f"Section '{data.section}' not found")
    
    slot = await FindDatasbyQuery({"date": data.date}, {}, data.section)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    
    return output.SlotDetails(slot=[await serialize_event(slot)])


async def delete_slot(data: input.DeleteSlot) -> output.DeleteSlot:
    slot_data = await FindDatasbyQuery({"slot": data.slot}, {}, data.section)
    if not slot_data:
        raise HTTPException(status_code=404, detail=f"Slot '{data.slot}' not found")

    deleted = await DeleteSlotBySection({"slot": data.slot, "date": data.date}, data.section)
    if not deleted:
        raise HTTPException(status_code=400, detail="Failed to delete slot")

    student_name = slot_data.get("student", "").replace(" ", "_")
    if student_name:
        student_deleted = await DeleteSlotBySection({"slot": data.slot, "date": data.date}, student_name)
        if not student_deleted:
            raise HTTPException(status_code=400, detail="Student slot deletion failed")

    return output.DeleteSlot(message="Slot deleted successfully")


async def get_student_slots(student_name: str) -> output.GetStudentSlots:
    formatted_name = student_name.replace(" ", "_")

    if not await section_exists(formatted_name):
        raise HTTPException(status_code=404, detail="No slots found for this student")

    slots = await get_events_database(formatted_name)
    if not slots:
        raise HTTPException(status_code=404, detail="No slots found")

    serialized = [await serialize_event(slot) for slot in slots]
    return output.GetStudentSlots(slots=serialized)