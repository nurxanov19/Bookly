from fastapi import FastAPI
from src.books.routes import *
from src.auth.routes import user_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print('Server ishga tushmoqda ...')
    await init_db()
    yield
    print('Server to\'xtadi!!!')

version = 'v1'

app = FastAPI(
    title="Bookly", description="A REST API for a book review web search", 
    version=version
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(user_router, prefix=f"/api/{version}/auth", tags=['users'])