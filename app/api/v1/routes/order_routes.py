from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db.mongodb import db
from app.core.exceptions import NotFoundException, BadRequestException
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId


router = APIRouter(prefix="/api/v1/orders", tags=["Order Management"])



@router.post("/place")
async def place_order(user=Depends(get_current_user)):

    if not user.get("cart"):
        raise BadRequestException("Cart is empty")

    order = {
        "user_id": str(user["_id"]),
        "items": user["cart"],
        "status": "placed",
        "created_at": datetime.utcnow()
    }

    await db.orders.insert_one(order)

    # Clear cart after order
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"cart": []}}
    )

    return {"message": "Order placed successfully"}



@router.get("/")
async def order_history(user=Depends(get_current_user)):

    orders = []
    async for order in db.orders.find({"user_id": str(user["_id"])}):
        order["id"] = str(order["_id"])
        del order["_id"]
        orders.append(order)

    return orders



@router.get("/{order_id}")
async def track_order(order_id: str, user=Depends(get_current_user)):

    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        raise NotFoundException("Invalid order ID")

    order = await db.orders.find_one({
        "_id": obj_id,
        "user_id": str(user["_id"])
    })

    if not order:
        raise NotFoundException("Order not found")

    order["id"] = str(order["_id"])
    del order["_id"]

    return order


@router.put("/cancel/{order_id}")
async def cancel_order(order_id: str, user=Depends(get_current_user)):

    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        raise NotFoundException("Invalid order ID")

    order = await db.orders.find_one({
        "_id": obj_id,
        "user_id": str(user["_id"])
    })

    if not order:
        raise NotFoundException("Order not found")

    if order.get("status") == "cancelled":
        raise BadRequestException("Order already cancelled")

    await db.orders.update_one(
        {"_id": obj_id},
        {"$set": {"status": "cancelled"}}
    )

    return {"message": "Order cancelled successfully"}
