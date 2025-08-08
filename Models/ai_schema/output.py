from pydantic import BaseModel
from typing import Optional, List

class AiOutput(BaseModel):
    message: str
    links: Optional[List[str]]
