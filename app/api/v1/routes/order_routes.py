from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.db.mongodb import db
from datetime import datetime

router = APIRouter(prefix="/api/v1/orders", tags=["Order Management"])


@router.post("/place")
async def place_order(user=Depends(get_current_user)):
    if not user["cart"]:
        raise HTTPException(400, "Cart is empty")

    order = {
        "user_id": str(user["_id"]),
        "items": user["cart"],
        "status": "placed",
        "created_at": datetime.utcnow()
    }

    await db.orders.insert_one(order)

    await db.users.update_one({"_id": user["_id"]}, {"$set": {"cart": []}})

    return {"message": "Order placed successfully"}
