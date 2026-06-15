from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from books import books
from schemas import BookCreate, BookResponse, BookUpdate

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/books", response_model=list[BookResponse])
def get_books(
    author: str | None = None,
    min_price: Annotated[float | None, Query(gt=0)] = None,
) -> list[BookResponse]:
    result = books

    if author is not None:
        result = [book for book in result if book["author"].lower() == author.lower()]

    if min_price is not None:
        result = [book for book in result if book["price"] >= min_price]

    return result


@app.get("/books/count")
def get_books_count():
    return {"count": len(books)}


@app.get("/books/author/{author}", response_model=list[BookResponse])
def get_books_by_author(author: str):
    return [book for book in books if book["author"].lower() == author.lower()]


@app.post("/books", response_model=BookResponse)
def create_book(book: BookCreate) -> BookResponse:
    next_id = max((existing_book["id"] for existing_book in books), default=0) + 1
    new_book = {"id": next_id, **book.model_dump()}
    books.append(new_book)

    return new_book


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int) -> BookResponse:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/search")
def search_books(author: str):
    return [book for book in books if author.lower() in book["author"].lower()]


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookUpdate) -> BookResponse:
    book_index = None

    for index, book in enumerate(books):
        if book["id"] == book_id:
            book_index = index
            break

    if book_index is None:
        raise HTTPException(status_code=404, detail="Book not found")

    current_book = books[book_index].copy()

    for key, value in updated_book.model_dump(exclude_unset=True).items():
        current_book[key] = value

    books[book_index] = current_book

    return current_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)
            return {"message": "Deleted"}

    raise HTTPException(status_code=404, detail="Book not found")