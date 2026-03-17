from fastapi import Request, HTTPException, Depends, status
from server.settings import get_db
from sqlalchemy.orm import Session, selectinload
from .models import SessionModel, User, Role


def is_authenticated(session_token:Request, db:Session = Depends(get_db)):
    session_token = session_token.cookies.get("auth_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    session = db.query(SessionModel).options(
        selectinload(SessionModel.user).selectinload(User.permissions),
        selectinload(User.roles).selectinload(Role.permissions)).filter(
            SessionModel.token == session_token).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    return session.user

def has_permission(required_permission:list):
    def checker(user = Depends(is_authenticated)):
        user_permissions = [per.name for per in user.permissions]
        for per in user.roles.permissions:
            user_permissions.append(per.name)
        user_permissions = set(user_permissions)

        for req_per in required_permission:
            if req_per not in user_permissions:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied!")
        return True
    return checker
