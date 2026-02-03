from fastapi import APIRouter, HTTPException
from app.core.db import get_collection
from app.core.security import hash_password, verify_password, create_token
from app.models.user import Register, Login
from pymongo.errors import PyMongoError

router = APIRouter(prefix='/auth', tags=['auth'])
users = get_collection("users")

@router.post("/register")
async def register(data: Register):
    if await users.find_one({"email": data.email}):
        raise HTTPException(400, "Email already exists")

    new_user = data.model_dump()
    new_user["password"] = hash_password(data.password)

    try:
        result = await users.insert_one(new_user)
        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Failed to create user")
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    
    token = create_token(str(result.inserted_id))

    return {"access_token": token, "token_type": "bearer", "message": "User registered successfully"}


@router.post("/login")
async def login(data: Login):    
    user = await users.find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(401, "Invalid credentials")
    
    token = create_token(str(user['_id']))
    
    return {"access_token": token, "token_type": "bearer"}
