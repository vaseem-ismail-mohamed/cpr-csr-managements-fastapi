from pydantic import BaseModel
from typing import Optional

class AiInput(BaseModel):
    input: str
    name: Optional[str] = None