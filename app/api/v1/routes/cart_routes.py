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



@router.get("/")
async def view_cart(user=Depends(get_current_user)):
    return {"cart": user.get("cart", [])}


@router.put("/update/{book_id}")
async def update_cart(book_id: str, quantity: int, user=Depends(get_current_user)):
    await db.users.update_one(
        {"_id": user["_id"], "cart.book_id": book_id},
        {"$set": {"cart.$.quantity": quantity}}
    )
    return {"message": "Cart updated successfully"}


@router.delete("/remove/{book_id}")
async def remove_from_cart(book_id: str, user=Depends(get_current_user)):
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$pull": {"cart": {"book_id": book_id}}}
    )
    return {"message": "Book removed from cart"}
