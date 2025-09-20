from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ------------------------------
# Book Model
# ------------------------------
class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float

# In-memory database (list of books)
books_db = []

# ------------------------------
# Endpoints
# ------------------------------

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Book Shop API"}

# Add a book
@app.post("/book")
def add_book(book: Book):
    # check duplicate ID
    for b in books_db:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book ID already exists")
    books_db.append(book)
    return {"message": "Book added successfully", "book": book}

# Get all books
@app.get("/book")
def get_books():
    return books_db

# Get book by ID
@app.get("/book/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Update book by ID
@app.put("/book/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db[i] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
    raise HTTPException(status_code=404, detail="Book not found")

# Delete book by ID
@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            deleted_book = books_db.pop(i)
            return {"message": "Book deleted successfully", "book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")
