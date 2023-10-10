from fastapi import APIRouter, HTTPException, Path

from .crud import crud_boards as crud
from .models import BoardDB, BoardSchema, NoteDB
from datetime import datetime as dt
from typing import List

router = APIRouter()


@router.post("/", response_model=BoardDB, status_code=201)
async def create_board(payload: BoardSchema):
    """Create new Board"""
    board_id = await crud.post(payload)
    response_object = {
        "id": board_id,
        "title": payload.title,
    }
    return response_object


@router.get("/{id}/", response_model=BoardDB)
async def read_board(id: int = Path(..., gt=0), ):
    """Get Board by id """
    board = await crud.get(id)
    if not board:
        raise HTTPException(status_code=404, detail="board not found")

    return board


@router.get("/board_list/", response_model=list[BoardSchema])
async def get_boards(skip: int = 0, take: int = 20):
    """Fetch boards with pagination"""
    rows = await crud.get_boards(skip, take)
    return rows


@router.get("/", response_model=list[BoardSchema])
async def read_all_boards():
    """Get list of all Boards """
    return await crud.get_all()


@router.put("/{id}/", response_model=BoardDB)
async def update_board(payload: BoardSchema, id: int = Path(..., gt=0)):
    """Update board title"""
    board = await crud.get(id)
    if not board:
        raise HTTPException(status_code=404, detail="board not found")

    board_id = await crud.put(id, payload)

    response_object = {'id': board_id, 'title': payload.title}
    return response_object


@router.put("/add_note/{id}/", response_model=BoardDB)
async def add_note_to_board(notes_id: List[int], current_board_id: int = Path(..., gt=0)):
    """Add note to board id"""
    board = await crud.add_note_to_board(notes_id, current_board_id)
    if not board:
        raise HTTPException(status_code=404, detail="board not found")
    board_id = await crud.put(current_board_id, payload, board.created_date)
    response_object = {'id': board_id, 'title': payload.title, "created_date": board.created_date}
    return response_object


@router.delete("/{id}/", response_model=BoardDB)
async def delete_board(id: int = Path(..., gt=0)):
    """Delete Board with id number"""
    board = await crud.get(id)
    if not board:
        raise HTTPException(status_code=404, detail="board not found")
    await crud.delete(id)
    return board
