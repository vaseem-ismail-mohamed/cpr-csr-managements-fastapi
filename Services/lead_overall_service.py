from DataBase.db import users_collection, Status_db, bookings_collection, Details_db, score_db, calenderdb
import calendar
from datetime import datetime

existing_sections = ["A", "B", "C"]

async def get_users_stats():
    student_A = await users_collection.count_documents({"role": "Student", "section": "A"})
    student_B = await users_collection.count_documents({"role": "Student", "section": "B"})
    student_C = await users_collection.count_documents({"role": "Student", "section": "C"})
    admin_A = await users_collection.count_documents({"role": "Admin", "section": "A"})
    admin_B = await users_collection.count_documents({"role": "Admin", "section": "B"})
    admin_C = await users_collection.count_documents({"role": "Admin", "section": "C"})  # Fix: was "B"

    users_statistics = {
        "student_a": student_A,
        "student_b": student_B,
        "student_c": student_C,
        "admin_a": admin_A,
        "admin_b": admin_B,
        "admin_c": admin_C,
    }

    return users_statistics

# ✅ Reusable month name to number converter
def get_month_number(month: str) -> int:
    try:
        month = month.strip().capitalize()
        month_num = list(calendar.month_name).index(month)
        if month_num == 0:
            raise ValueError
        return month_num
    except ValueError:
        raise Exception("Invalid month name")

async def get_booking_stats_by_month(month: str):
    year = datetime.now().year
    int_month = get_month_number_slots(month)

    # Convert to string-based date (if your DB stores "date" as strings like "2025-01-01")
    start_date_str = f"{year}-{int_month:02d}-01"
    end_date_str = (
        f"{year + 1}-01-01" if int_month == 12 else f"{year}-{int_month + 1:02d}-01"
    )

    query = {
        "date": {
            "$gte": start_date_str,
            "$lt": end_date_str
        }
    }

    result = {}

    for section in existing_sections:
        collection = calenderdb[section]
        count = await collection.count_documents(query)
        result[section] = count
        print(f"[{section}] → Count: {count}")

    return {"bookings_by_section": result}

async def get_feedback_by_month(month: str):
    year = datetime.now().year
    month_num = get_month_number(month)
    feedbacks = 0

    users = await users_collection.find({}, {'_id': 0, 'email': 1}).to_list(length=None)
    for user in users:
        start_timestamp = datetime(year, month_num, 1)
        end_timestamp = datetime(year + 1, 1, 1) if month_num == 12 else datetime(year, month_num + 1, 1)

        query = {
            "timestamp": {
                "$gte": start_timestamp,
                "$lt": end_timestamp
            }
        }

        collection = user["email"].replace(".", "_").replace("@", "_")
        count = await Details_db[collection].count_documents(query)
        feedbacks += count

    return {"feedbacks": feedbacks}

def get_month_number_slots(month_name: str) -> int:
    return datetime.strptime(month_name, "%B").month

async def get_slots_by_month(month: str):
    month_num = get_month_number_slots(month)
    year = datetime.now().year

    start_date_str = f"{year}-{month_num:02d}-01"
    if month_num == 12:
        end_date_str = f"{year + 1}-01-01"
    else:
        end_date_str = f"{year}-{month_num + 1:02d}-01"

    query = {
        "date": {
            "$gte": start_date_str,
            "$lt": end_date_str
        }
    }

    print("Query:", query)

    count = await bookings_collection.count_documents(query)
    print("Count:", count)

    return {"slots": count}


async def get_scores_by_month(month: str):
    month_num = get_month_number(month)
    year = datetime.now().year

    start_timestamp = datetime(year, month_num, 1)
    end_timestamp = datetime(year + 1, 1, 1) if month_num == 12 else datetime(year, month_num + 1, 1)

    query = {
        "timestamp": {
            "$gte": start_timestamp,
            "$lt": end_timestamp
        }
    }

    counts = []
    for section in existing_sections:
        collection_name = f"Section_{section}"
        collection = score_db[collection_name]

        count = await collection.count_documents(query)
        counts.append({f"Section-{section}": count})

    return {"scores": counts}
