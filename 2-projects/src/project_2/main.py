from fastapi import Body, FastAPI, Path, Query, HTTPException
from starlette import status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: date

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
    
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None, gt=1)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=11)
    published_date: date = Field(gt=date(1900,1,1), lt=date(2025,12,31))

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Animal Farm",
                "author": "George Orwell",
                "description": "Short story of a pig and some animals",
                "rating": 10,
                "published_date": date(1965,1,31)
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'Coding with Roby', 'A very nice book', 5, date(2000, 1, 1)),
    Book(2, 'Be fast with FastAPI', 'Coding with Roby', 'A great book', 5, date(2000,12,10)),
    Book(3, 'Surely Youre Joiking Mr. Feynman!', 'Richard Feynman', 'A great book', 10, date(1964,10,1)),
    Book(4, 'Feynman Lectures on Physics', 'Richard Feynman', 'Best book ever', 10, date(1960,1,1)),
    Book(5, '1984', 'George Orwell', 'A Masterpiece', 10, date(1970,10,10)),
    Book(6, 'Animal Farm', 'George Orwell', 'Very Good', 9, date(1963,12,1))
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/published_date/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: date = Query(gt=date(1990,1,1), lt=date(2025,12,31))):
    return [book for book in BOOKS if book.published_date >= published_date]


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(404, "Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=11)):
    return [book for book in BOOKS if book.rating >= book_rating]


@app.post("/books/create-book", status_code=status.HTTP_204_NO_CONTENT)
async def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    new_book.id = find_book_id()

@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if book.id == BOOKS[i].id:
            updated_book = Book(**book.model_dump())
            BOOKS[i] = updated_book
    raise HTTPException(404, "Book not found")

@app.delete("/books/delete-book", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if book.id == BOOKS[i].id:
            return BOOKS.pop(i)
    return HTTPException(404, "Book not found")

def find_book_id():
    return 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1