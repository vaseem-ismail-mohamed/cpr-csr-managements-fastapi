from bson import ObjectId


async def StudentsList(students, status_data):
    students_list = []
    for student in students:
        student_status = status_data.get(str(student['_id']), "Not Complete")
        students_list.append({
            "name": student["name"].strip(),
            "email": student["email"].strip(),
            "status": student_status
        })
    return students_list


async def StatusUpdatetoDB(status_updates, month_collection):
    for update in status_updates:
        student_id = update.get('student_id')
        status = update.get('status')
        if student_id and status:
            await month_collection.update_one(
                {"_id": ObjectId(student_id)},
                {"$set": {"status": status}},
                upsert=True
            )
    return True