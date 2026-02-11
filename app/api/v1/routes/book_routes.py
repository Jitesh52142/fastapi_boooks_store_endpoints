from fastapi import APIRouter, Query
from app.db.mongodb import db
from bson import ObjectId

router = APIRouter(prefix="/api/v1/books", tags=["Book Catalog"])


@router.get("/")
async def browse_books(
    title: str = None,
    author: str = None,
    genre: str = None,
    min_price: float = None,
    max_price: float = None,
):
    query = {}

    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
    if genre:
        query["genre"] = genre
    if min_price or max_price:
        query["price"] = {}
        if min_price:
            query["price"]["$gte"] = min_price
        if max_price:
            query["price"]["$lte"] = max_price

    books = []
    async for book in db.books.find(query):
        book["id"] = str(book["_id"])
        del book["_id"]
        books.append(book)

    return books
