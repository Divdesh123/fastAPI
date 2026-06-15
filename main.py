from fastapi import FastAPI, HTTPException
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


@app.get("/books/count")
def get_books_count():
    return {"count": len(books)}


@app.get("/books/author/{author}")
def get_books_by_author(author: str):
    result = []

    for book in books:
        if book["author"].lower() == author.lower():
            result.append(book)

    return result


@app.post("/books")
def create_book(book: Book):
    for existing_book in books:
        if existing_book["id"] == book.id:
            raise HTTPException(status_code=400, detail="Book id already exists")

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
    book_index = None

    for index, book in enumerate(books):
        if book["id"] == book_id:
            book_index = index
            break

    if book_index is None:
        return {"error": "Book not found"}

    if updated_book.id != book_id:
        for existing_index, existing_book in enumerate(books):
            if existing_book["id"] == updated_book.id and existing_index != book_index:
                raise HTTPException(status_code=400, detail="Book id already exists")

    books[book_index] = updated_book.model_dump()

    return {"message": "Updated"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    removed = False

    for index in range(len(books) - 1, -1, -1):
        if books[index]["id"] == book_id:
            books.pop(index)
            removed = True

    if removed:
        return {"message": "Deleted"}

    return {"error": "Book not found"}