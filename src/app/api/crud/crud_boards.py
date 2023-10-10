from ..models import BoardSchema, BoardDB
from ...db import database, boards, notes
from datetime import datetime as dt


async def add_note_to_board(note_id: list[int], id: int):
    breakpoint()
    query = boards.update().join(notes, boards.c.id == notes.c.board_id).where(id == boards.c.id).values(
        notes_id=note_id)
    return await database.execute(query=query)


async def post(payload: BoardSchema):
    query = boards.insert().values(title=payload.title, created_date=dt.now())
    return await database.execute(query=query)


async def get(id: int):
    query = boards.select().join(notes, boards.c.id == notes.c.board_id).where(id == boards.c.id)
    res = await database.fetch_one(query=query)
    return res


async def get_boards(skip: int, take: int):
    query = boards.select().offset(skip).limit(take)
    return await database.fetch_all(query=query)


async def get_all():
    query = boards.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: BoardSchema, created_date: dt.now()):
    query = (boards
             .update()
             .where(id == boards.c.id)
             .values(title=payload.title, created_date=created_date, updated_date=dt.now())
             .returning(boards.c.id)
             )
    return await database.execute(query=query)


async def delete(id: int):
    query = boards.delete().where(id == boards.c.id)
    return await database.execute(query=query)
