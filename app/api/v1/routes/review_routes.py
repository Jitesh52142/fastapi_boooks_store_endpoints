from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.mongodb import db
from datetime import datetime

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
