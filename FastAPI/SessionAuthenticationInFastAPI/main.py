from fastapi import FastAPI
from accounts.views import auth
import uvicorn



app = FastAPI()
app.include_router(auth, prefix="/auth", tags=["Authentication"])




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)