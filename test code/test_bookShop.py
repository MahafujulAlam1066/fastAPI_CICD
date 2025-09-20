import sys
import os

# Add 'source code' folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source code")))

from fastapi.testclient import TestClient
from bookShop import app  # Make sure 'app' is the FastAPI instance in bookShop.py

client = TestClient(app)


# Test home endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Book Shop API"}


# Test adding a book
def test_add_book():
    book = {"id": 1, "title": "Test Book", "author": "Author A", "price": 10.5}
    response = client.post("/book", json=book)
    assert response.status_code == 200
    assert response.json()["message"] == "Book added successfully"
    assert response.json()["book"] == book


# Test adding duplicate book
def test_add_duplicate_book():
    book = {"id": 1, "title": "Test Book", "author": "Author A", "price": 10.5}
    response = client.post("/book", json=book)
    assert response.status_code == 400
    assert response.json()["detail"] == "Book ID already exists"


# Test getting all books
def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


# Test getting book by ID
def test_get_book_by_id():
    response = client.get("/book/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


# Test getting a book that does not exist
def test_get_book_not_found():
    response = client.get("/book/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


# Test updating a book
def test_update_book():
    updated_book = {"id": 1, "title": "Updated Book", "author": "Author B", "price": 12.0}
    response = client.put("/book/1", json=updated_book)
    assert response.status_code == 200
    assert response.json()["message"] == "Book updated successfully"
    assert response.json()["book"] == updated_book


# Test deleting a book
def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
    assert response.json()["book"]["id"] == 1


# Test deleting a book that does not exist
def test_delete_book_not_found():
    response = client.delete("/book/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
