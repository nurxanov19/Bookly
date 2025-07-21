from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import BookModel, BookUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.services import BookServices
from src.books.models import Book
from src.db.main import get_session
from typing import List


book_router = APIRouter()
book_service = BookServices()

@book_router.get("/", response_model=List[Book])
async def get_all_book(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data: BookModel, session: AsyncSession = Depends(get_session))-> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get("/{book_uid}", status_code=status.HTTP_200_OK )
async def get_book(book_uid: int, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
@book_router.patch("/{book_uid}", status_code=status.HTTP_200_OK)
async def update_book(book_uid: str, book_updata_data: BookUpdateModel, session: AsyncSession=Depends(get_session)):
    updated_book = await book_service.update_book(book_uid, book_updata_data, session)

    if updated_book:
        return updated_book
    
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Book Not Found")

@book_router.delete("/{book_uid}")
async def delete_book(book_uid: int, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.get_books(book_uid, session)
    
    if book_to_delete:
        book_service.delete_book(book_uid, session)

    else:
        return None
