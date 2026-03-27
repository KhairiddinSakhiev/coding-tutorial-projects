from models.users import User
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

def get_user(db:Session, username:str=None, user_id:int=None):
    print("test", username, user_id)
    if not username and not user_id:
        raise HTTPException(detail="Please set username or user_id", status_code=status.HTTP_400_BAD_REQUEST)

    user = db.query(User).filter(or_(User.id == user_id, User.username==username)).first()
    return user

def create_user(user_data, db):
    user_exists = get_user(username=user_data.username, db=db)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")
    user = User(username=user_data.username, password=user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user