from fastapi import APIRouter, Query
from app.db.mongodb import db
from bson import ObjectId
from fastapi import Depends, HTTPException
from app.core.security import get_current_user
from app.core.exceptions import NotFoundException, ForbiddenException
from datetime import datetime

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




@router.get("/{book_id}")
async def get_book_details(book_id: str):
    book = await db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise NotFoundException("Book not found")

    book["id"] = str(book["_id"])
    del book["_id"]
    return book


@router.post("/")
async def create_book(
    title: str,
    author: str,
    genre: str,
    price: float,
    stock: int,
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise ForbiddenException("Only admin can create books")

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "price": price,
        "stock": stock,
        "rating": 0,
        "created_at": datetime.utcnow()
    }

    await db.books.insert_one(book)
    return {"message": "Book created successfully"}


@router.put("/{book_id}")
async def update_book(
    book_id: str,
    price: float,
    stock: int,
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise ForbiddenException("Only admin can update books")

    result = await db.books.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": {"price": price, "stock": stock}}
    )

    if result.matched_count == 0:
        raise NotFoundException("Book not found")

    return {"message": "Book updated successfully"}


@router.delete("/{book_id}")
async def delete_book(book_id: str, user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise ForbiddenException("Only admin can delete books")

    result = await db.books.delete_one({"_id": ObjectId(book_id)})

    if result.deleted_count == 0:
        raise NotFoundException("Book not found")

    return {"message": "Book deleted successfully"}