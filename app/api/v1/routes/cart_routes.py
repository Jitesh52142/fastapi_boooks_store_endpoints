from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.db.mongodb import db
from bson import ObjectId

router = APIRouter(prefix="/api/v1/cart", tags=["Shopping Cart"])


@router.post("/add/{book_id}")
async def add_to_cart(book_id: str, quantity: int, user=Depends(get_current_user)):
    book = await db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(404, "Book not found")

    await db.users.update_one(
        {"_id": user["_id"]},
        {"$push": {"cart": {"book_id": book_id, "quantity": quantity}}}
    )

    return {"message": "Book added to cart"}
