from fastapi import FastAPI
from pydantic import BaseModel

from books import books

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/books")
def get_books():
    return books


@app.post("/books")
def create_book(book: Book):
    books.append(book.model_dump())

    return {"message": "Book added"}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    return {"error": "Book not found"}


@app.get("/search")
def search_books(author: str):
    result = []

    for book in books:
        if author.lower() in book["author"].lower():
            result.append(book)

    return result


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books[index] = updated_book.model_dump()
            return {"message": "Updated"}

    return {"error": "Book not found"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)
            return {"message": "Deleted"}

    return {"error": "Book not found"}