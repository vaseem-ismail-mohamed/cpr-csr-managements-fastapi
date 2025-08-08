from pydantic import BaseModel
from typing import List, Dict

class GetLeadOverallStatistics(BaseModel):
    users_statistics: Dict[str, int]
    calender_bookings: Dict[str, int]
    feedbacks: int
    meet_slots: int
    scores: List[Dict[str, int]]
