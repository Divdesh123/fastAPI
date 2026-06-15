from fastapi import FastAPI

from books import books

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/books")
def get_books():
    return books


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