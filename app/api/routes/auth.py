from fastapi import APIRouter, HTTPException, Depends
from app.core.db import get_collection
from app.core.security import hash_password, verify_password, create_token, get_current_user
from app.models.users import Register, Login

router = APIRouter()
users = get_collection("users")

@router.post("/register")
async def register(data: Register):
    if await users.find_one({"email": data.email}):
        raise HTTPException(400, "Email already exists")

    await users.insert_one({
        "username": data.username,
        "email": data.email,
        "password": hash_password(data.password)
    })

    token = create_token(data.email)

    return {"access_token": token, "token_type": "bearer", "message": "User registered successfully", "user": {"username": data.username, "email": data.email}}


@router.post("/login")
async def login(data: Login):
    user = await users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(data.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}
