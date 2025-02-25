from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Tuple
from typing_extensions import Literal


class TodoItem(BaseModel):
    title: str
    is_open: bool


class TodoList(BaseModel):
    title: str
    items: List[TodoItem]
    id: str  #
    sk: str  # status
    status: Literal["arch", "ip", "bcklg"]

    @property
    def readable_status(self):
        return {
            "arch": "Archived",
            "ip": "In progress",
            "bcklg": "Backlog",
        }.get(self.status, "Unknown")


class User(BaseModel):
    user_id: str
    name: str
