from pydantic import BaseModel
from typing import List, Optional

class GoalItem(BaseModel):
    label: str
    goal: str

class AddMultipleGoals(BaseModel):
    section: str
    to: str
    from_: Optional[str] = "Admin"
    goals: List[GoalItem]
    month: Optional[str] = None