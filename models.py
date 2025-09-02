from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    deadline: datetime
    done: bool
    
