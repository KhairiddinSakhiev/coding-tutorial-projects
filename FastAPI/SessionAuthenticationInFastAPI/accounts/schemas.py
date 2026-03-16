from pydantic import BaseModel

class SetPermissionToUserSchema(BaseModel):
    user_id:int
    permissions:list[int]