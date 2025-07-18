from sqlmodel import Field, Column, SQLModel, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime

class Book(SQLModel, table=True):
    __tablename__ = 'books'
    uid: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=True,
            primary_key=True,
            default=uuid.uuid4()
        )
    )
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))

    def ___repr__(self):
        return f"Book > {self.title } ({self.author})"
