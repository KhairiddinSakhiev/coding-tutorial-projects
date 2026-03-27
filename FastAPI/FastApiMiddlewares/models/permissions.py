from .base import AbstractBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Table, Column, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User

class Permission(AbstractBase):
    __tablename__ = "permissions"
    
    title:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description:Mapped[str] = mapped_column(String, nullable=False)
    
    users:Mapped[list["User"]] = relationship("User", back_populates="permissions", secondary="users_permissions")
    

users_permissions = Table(
    "users_permissions", AbstractBase.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)