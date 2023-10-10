from ..models import NoteSchema, NoteDB
from ...db import database, notes, engine, boards
from datetime import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession


async def post(payload: NoteSchema):
    query = notes.insert().values(text=payload.text, views=0, created_date=dt.now(), board_id=payload.board_id)
    return await database.execute(query=query)


# async def add_note_to_board(note_id: int, board_id):
#     await database.execute(query=(boards
#                                   .update()
#                                   .where(board_id == boards.c.id)
#                                   .values(notes_id=note_id))
#                                   )


async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)


async def get_notes(skip: int, take: int):
    query = notes.select().offset(skip).limit(take)
    return await database.fetch_all(query=query)


async def get_all():
    query = notes.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: NoteSchema, created_date: dt.now()):
    query = (notes
             .update()
             .where(id == notes.c.id)
             .values(text=payload.text, created_date=created_date, updated_date=dt.now())
             .returning(notes.c.id)
             )
    return await database.execute(query=query)


async def update_views(id: int, payload: NoteSchema):
    view = payload.views + 1
    query = (notes
             .update()
             .where(id == notes.c.id)
             .values(views=view)
             .returning(notes.c.id)
             )
    return await database.execute(query=query)


async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)
