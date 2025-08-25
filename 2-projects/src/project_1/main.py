from fastapi import Body, FastAPI
import json

# import the books.json file into a dictionary
with open("books.json") as f:
    books = json.load(f).get("books", [])

app = FastAPI()

@app.get("/books")
async def read_all_books():
    """
    Endpoint to read all books from the books.json file.
    Returns:
        A list of all books.
    """
    return books

# Example of a path parameter
@app.get("/books/{category}")
async def read_books_by_category(category: str):
    """
    Endpoint to read all books by category
    Returns:
        A list of books in the specified category.
    """
    return [book for book in books if book.get("category") == category]

# Example of a query parameter
@app.get("/books/")
async def read_books_by_author(author: str):
    """
    Endpoint to read all books by author
    Returns:
        A list of books by the specified author.
    """
    return [book for book in books if book.get("author") == author]

# Example of a path and query parameter
# Note the / to differentiate from the previous endpoint
@app.get("/books/{author}/") 
async def read_books_by_authoir_and_category(author: str, category: str):
    """
    Endpoint to read all books by author and category
    Returns:
        A list of books by the specified author in the specified category.
    """
    return [
        book for book in books 
        if book.get("author") == author \
            and book.get("category") == category
    ]

# Example post request with book body
@app.post("/books/create_book")
async def create_book(new_book: dict = Body()):
    """
    Endpoint to create a new book.
    Args:
        new_book: A dictionary containing the book details.
    Returns:
        The newly created book.
    """
    books.append(new_book)
    return new_book

# Example put request to update a book
@app.put("/books/update_book")
def update_book(updated_book: dict = Body()):
    """
    Endpoint to update a book
    Args:
        update_book: A dictionary containing the book details
    Returns:
        The updated book
    """

    for i in range(len(books)):
        if books[i].get("title").casefold() == updated_book.get("title").casefold():
            books[i] = updated_book
            return updated_book
    return {
        "error": "book not found"
    }

# Example of a delete request
@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    """
    Endpoint to delete a book by title
    Args:
        book_title: title of the book to delete
    """
    for i in range(len(books)):
        if books[i].get("title").casefold() == book_title.casefold():
            return books.pop(i)
    return {
        "error": f"book title '{book_title}' not found"
    }





