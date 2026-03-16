from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session, selectinload
from .models import *
from .security import *
from .serivces import *
from .schemas import *
from .permissions import get_current_user
from server.settings import get_db


auth = APIRouter()

@auth.post("/register")
async def add_user(username:str, password:str, confirm_password:str):
    if password != confirm_password:
        raise HTTPException(detail="Passwords don't match", status_code=status.HTTP_400_BAD_REQUEST )
    hash_passowrd = hash_password(password=password) 
    new_user = User(username=username, password=hash_passowrd)
    with get_connection() as db:
        user=db.query(User).filter(User.username==username).first()
        if user:
            raise HTTPException(detail="User already exists", status_code=status.HTTP_400_BAD_REQUEST)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

@auth.post("/login")
async def login_user(response:Response, username: str, password: str):
    user_exists = get_user(username=username)
    if user_exists is not None:
        print("test", user_exists.password, user_exists.username)
        print(type(password))
        is_password_correct = verify_password(password=password, hashed_password=user_exists.password)
        if not is_password_correct:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
        token = generate_token(user_id=user_exists.id)
        response.set_cookie("auth_token", token.token)
        return {"msg":"Use loged In"}
    return HTTPException(detail="Invalid credentials or user not found", status_code=status.HTTP_400_BAD_REQUEST)
        
    
@auth.post("/logout")
async def logout_view(respose:Response, user = Depends(get_current_user)):
    respose.delete_cookie("auth_token")
    return "Logged out"


@auth.post("/set-permissions-to-user")
async def set_permissions_to_user_view(data:SetPermissionToUserSchema, db:Session = Depends(get_db)):
    user = db.query(User).options(
        selectinload(User.permissions)).filter(User.id==data.user_id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with id: {data.user_id} not found") 
    permissions = db.query(Permissions).filter(Permissions.id.in_(data.permissions)).all()
    if permissions is not None:
        for per in permissions:
            user.permissions.append(per)
        db.commit()
        return {"msg": "Success!"}
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="permissions with these ids not found")