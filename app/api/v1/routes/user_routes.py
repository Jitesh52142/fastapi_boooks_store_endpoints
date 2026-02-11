from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserRegister, UserLogin
from app.db.mongodb import db
from app.core.security import hash_password, verify_password, create_access_token
from bson import ObjectId

router = APIRouter(prefix="/api/v1/users", tags=["User Management"])


@router.post("/register", status_code=201)
async def register(user: UserRegister):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(400, "Email already registered")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["role"] = "user"
    user_dict["cart"] = []

    result = await db.users.insert_one(user_dict)

    return {"message": "User registered successfully"}


@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(400, "Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(400, "Invalid credentials")

    token = create_access_token({"sub": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}
