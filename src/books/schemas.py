from pydantic import BaseModel
from datetime import date
import uuid
from typing import Optional


class BookModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

    class Config:
        from_attributes = True


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    page_count: Optional[int]
    language: Optional[str]