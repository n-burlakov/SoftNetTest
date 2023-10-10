from fastapi import APIRouter, HTTPException, Path, Depends, FastAPI

from .crud import crud_notes as crud
from .models import NoteDB, NoteSchema, BoardSchema
from datetime import datetime as dt
from ..db import notes, boards
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await crud.post(payload)
    # await crud.add_note_to_board(note_id=note_id, board_id=payload.board_id)
    response_object = {
        "id": note_id,
        "text": payload.text,
        "board id": payload.board_id
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0), ):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.update_views(id=id, payload=note)
    return await crud.get(id)


@router.get("/notes/", response_model=NoteDB)
async def get_notes(skip: int = 0, take: int = 20):
    """Fetch notes with pagination"""
    rows = await crud.get_notes(skip, take)
    return rows


@router.get("/", response_model=list[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{id}/", response_model=NoteDB)
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await crud.put(id, payload, note.created_date)

    response_object = {'id': note_id, 'text': payload.text, "created_date": note.created_date}
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.delete(id)
    return note
