from DataBase.db import Details_db
from datetime import datetime


async def InsertSenderReceiver(sender_email: str, receiver_email: str, feedback: str) -> bool:
    sender_col_name = sender_email.replace('.', '_').replace('@', '_')
    receiver_col_name = receiver_email.replace('.', '_').replace('@', '_')

    sender_col = Details_db[sender_col_name]
    receiver_col = Details_db[receiver_col_name]

    feedback_doc = {
        "from": sender_email,
        "to": receiver_email,
        "textcontent": feedback,
        "timestamp": datetime.utcnow()
    }

    result1 = await sender_col.insert_one(feedback_doc)
    result2 = await receiver_col.insert_one(feedback_doc)

    return result1.inserted_id is not None and result2.inserted_id is not None


async def ValidateDBandGetData(collection_name: str):
    feedback_collection = Details_db[collection_name]
    print('feedback collection :', feedback_collection)
    return await feedback_collection.find({}, {"_id": 0}).to_list(length=None)