import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    ForeignKey,
    create_engine,
)
from sqlalchemy.sql import func

from databases import Database


DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()


notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String(500)),
    Column("views", Integer, default=0),
    Column("created_date", DateTime, default=func.now(), nullable=False),
    Column("updated_date", DateTime, default=func.now(), nullable=False),
    Column("board_id", Integer, ForeignKey("boards.id")),
)

boards = Table(
    "boards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
    Column("updated_date", DateTime, default=func.now(), nullable=False),
    # Column("notes_id", ForeignKey("notes.id"))
)


database = Database(DATABASE_URL)
