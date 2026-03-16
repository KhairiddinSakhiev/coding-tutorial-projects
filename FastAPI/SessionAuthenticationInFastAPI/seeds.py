from server.base import AbstractBase
from accounts.models import *
from server.settings import get_connection
from datetime import datetime

def seed_permissions():
    tables = AbstractBase.__subclasses__()
    actions = ["read", "create", "update", "delete"]
    permissions = []
    for table in tables:
        for a in actions:
            permissions.append({
                "name": f"{table.__name__.lower()}:{a}",
                "descption": f"Can {a} {table.__name__.lower()}",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
    with get_connection() as session:
        session.execute(Permissions.__table__.insert(), permissions)
        session.commit()
    print(permissions)
    
    
    
seed_permissions()