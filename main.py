from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional, List
from fastapi.exceptions import HTTPException


app = FastAPI()


books = [
    {
        "id": 1,
        "title": "Think Python",
        "author": "Allen B. Downey",
        "publisher": "O'Reilly Media",
        "published_date": "2021-01-01",
        "page_count": 1234,
        "language": "English"
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-01",
        "page_count": 464,
        "language": "English"
    },
    {
        "id": 3,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "publisher": "Addison-Wesley Professional",
        "published_date": "1999-10-20",
        "page_count": 352,
        "language": "English"
    },
    {
        "id": 4,
        "title": "Design Patterns",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "publisher": "Addison-Wesley Professional",
        "published_date": "1994-10-21",
        "page_count": 395,
        "language": "English"
    },
    {
        "id": 5,
        "title": "Cracking the Coding Interview",
        "author": "Gayle Laakmann McDowell",
        "publisher": "CareerCup",
        "published_date": "2015-07-01",
        "page_count": 700,
        "language": "English"
    }
]


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


@app.get('/books', response_model=List[Book])
async def get_all_books():
    return books


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: Book) -> dict:

    new_book = book_data.model_dump()
    books.append(new_book)

    return new_book


@app.get('/book/{book_id}')
async def get_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/book/{book_id}')
async def update_book(book_id: int) -> dict:
    pass 