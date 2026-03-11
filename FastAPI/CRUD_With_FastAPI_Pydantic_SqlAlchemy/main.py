from fastapi import FastAPI, HTTPException, status
import uvicorn
from models import *
from db_config import get_connection


app = FastAPI()


@app.get("/say_hello")
async def say_hello():
    return {"message": "Hello world!"}


@app.post("/add-user")
async def add_user(username:str, password:str, confirm_password:str):
    if password != confirm_password:
        raise HTTPException(detail="Passwords don't match", status_code=status.HTTP_400_BAD_REQUEST ) 
    new_user = User(username=username, password=password)
    with get_connection() as db:
        user=db.query(User).filter(User.username==username).first()
        if user:
            raise HTTPException(detail="User already exists", status_code=status.HTTP_400_BAD_REQUEST)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)