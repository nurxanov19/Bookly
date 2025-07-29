from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import BookModel, BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.services import BookServices

from src.db.main import get_session
from typing import List
from src.auth.dependencies import AccessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = BookServices()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))


@book_router.get("/", response_model=List[BookModel], dependencies=[role_checker])
async def get_all_book(session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookModel, dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), 
                    user_details=Depends(access_token_bearer))-> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get("/{book_uid}", status_code=status.HTTP_200_OK, response_model=BookModel, dependencies=[role_checker] )
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
@book_router.patch("/{book_uid}", status_code=status.HTTP_200_OK, response_model=BookModel, dependencies=[role_checker])
async def update_book(book_uid: str, book_updata_data: BookUpdateModel, session: AsyncSession=Depends(get_session),
                      user_details=Depends(access_token_bearer)):
    updated_book = await book_service.update_book(book_uid, book_updata_data, session)

    if updated_book:
        return updated_book
    
    else:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Book Not Found")

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    deleted_book = await book_service.delete_book(book_uid, session)
    
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book Not Found')
    



    
