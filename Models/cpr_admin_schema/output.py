from pydantic import BaseModel

class UpdateMonthlyStatus(BaseModel):
    message: str