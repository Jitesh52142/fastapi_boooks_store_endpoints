from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.mongodb import db
from datetime import datetime
from app.core.exceptions import BadRequestException



router = APIRouter(prefix="/api/v1/reviews", tags=["Reviews & Ratings"])


@router.post("/{book_id}")
async def submit_review(book_id: str, rating: int, comment: str, user=Depends(get_current_user)):
    review = {
        "book_id": book_id,
        "user_id": str(user["_id"]),
        "rating": rating,
        "comment": comment,
        "created_at": datetime.utcnow()
    }

    await db.reviews.insert_one(review)

    return {"message": "Review submitted"}





@router.post("/{book_id}")
async def submit_review(book_id: str, rating: int, comment: str, user=Depends(get_current_user)):
    if rating < 1 or rating > 5:
        raise BadRequestException("Rating must be between 1 and 5")

    review = {
        "book_id": book_id,
        "user_id": str(user["_id"]),
        "rating": rating,
        "comment": comment
    }

    await db.reviews.insert_one(review)

    return {"message": "Review submitted successfully"}


@router.get("/{book_id}")
async def get_reviews(book_id: str):
    reviews = []
    async for review in db.reviews.find({"book_id": book_id}):
        review["id"] = str(review["_id"])
        del review["_id"]
        reviews.append(review)

    return reviews
