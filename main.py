from fastapi import FastAPI

from books import books

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/books")
def get_books():
    return books