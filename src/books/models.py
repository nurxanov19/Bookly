from sqlmodel import Field, Column, SQLModel, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, date

class Book(SQLModel, table=True):
    __tablename__ = 'books'
    uid: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def ___repr__(self):
        return f"Book > {self.title } ({self.author})"
