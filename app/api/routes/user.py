from fastapi import APIRouter, HTTPException, Depends
from app.core.db import get_collection
from app.core.security import get_current_user
from bson import ObjectId
from app.models.user import UserResponse
from pymongo.errors import PyMongoError

router = APIRouter(prefix='/user', tags=['user'])

users = get_collection("users")

@router.get("/me", response_model=UserResponse)
async def me(user_id: str = Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = await users.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["id"] = str(user["_id"])

    return user
