from fastapi import Request, HTTPException
from server.settings import get_connection
from .models import SessionModel


def get_current_user(session_token:Request):
    session_token = session_token.cookies.get("auth_token")
    with get_connection() as db:
        if not session_token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        session = db.query(SessionModel).filter(SessionModel.token == session_token).first()
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        return session.user