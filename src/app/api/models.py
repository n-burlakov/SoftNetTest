from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class NoteSchema(BaseModel):
    text: str = Field(..., min_length=3, max_length=500)
    board_id: Optional[int]


class NoteDB(NoteSchema):
    id: int
    views: int = 0
    created_date: Optional[datetime] = datetime.now()
    updated_date: Optional[datetime] = datetime.now()


class BoardSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)


class BoardDB(BoardSchema):
    id: int
    notes_id: Optional[NoteDB]
    created_date: Optional[datetime] = datetime.now()
    updated_date: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True
