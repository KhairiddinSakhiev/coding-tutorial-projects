from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserOut
from core.settings import get_db
from services.users import create_user



user_route = APIRouter()

@user_route.post("/register", response_model=UserOut)
async def register_view(user_data:UserCreate, db:Session=Depends(get_db)):
    user = create_user(user_data=user_data, db=db)
    return user

@user_route.get("/test")
async def test_view():
    return "hello world"