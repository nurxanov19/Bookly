from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    polisher: str
    polished_date: str
    page_count: int
    language: str


class BookCreateModel(BaseModel):
    title: str
    author: str
    polisher: str
    polished_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    polisher: str
    page_count: int
    language: str