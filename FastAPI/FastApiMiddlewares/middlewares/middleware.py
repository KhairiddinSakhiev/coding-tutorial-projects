from fastapi import Request
import time

async def request_proccess_time(request:Request, call_next):
    current_time = time.time()
    response = await call_next(request)
    total = time.time() - current_time
    response.headers["X-Proccess-Time"] = str(total)
    return response