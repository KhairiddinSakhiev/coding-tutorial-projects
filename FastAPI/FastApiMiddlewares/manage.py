from fastapi import FastAPI
import uvicorn
from views.users import user_route
from middlewares.middleware import request_proccess_time


app = FastAPI()
app.middleware("http")(request_proccess_time)
app.include_router(
    router=user_route,
    prefix="/auth/v1",
    tags=["Auth"]
)


if __name__ == "__main__":
    uvicorn.run("manage:app", host="127.0.0.1", port=8008)