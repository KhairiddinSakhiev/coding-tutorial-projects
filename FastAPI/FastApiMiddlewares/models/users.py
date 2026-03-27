from .base import AbstractBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .permissions import Permission, users_permissions


class User(AbstractBase):
    __tablename__ = "users"
    
    username:Mapped[String] = mapped_column(String(100), nullable=False, unique=True)
    password:Mapped[String] = mapped_column(String, nullable=False)
    
    permissions:Mapped[list["Permission"]] = relationship("Permission", back_populates="users", secondary="users_permissions")

