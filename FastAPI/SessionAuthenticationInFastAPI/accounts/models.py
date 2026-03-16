from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column, Boolean
import uuid
from server.base import AbstractBase

role_permissions = Table(
    'role_permissions', AbstractBase.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', ForeignKey("permissions.id"), primary_key=True)
)

user_roles = Table(
    'user_roles', AbstractBase.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('user_id', ForeignKey("users.id"), primary_key=True)
)

user_permissions = Table(
    'user_permissions', AbstractBase.metadata,
    Column('permission_id', ForeignKey('permissions.id'), primary_key=True),
    Column('user_id', ForeignKey("users.id"), primary_key=True)
)

class User(AbstractBase):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String)
    
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", uselist=False)
    sessions: Mapped[list["SessionModel"]] = relationship("SessionModel", back_populates="user")
    permissions: Mapped[list["Permissions"]] = relationship("Permissions", back_populates="users", secondary="user_permissions")
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="users", secondary="user_roles")
    
    def __repr__(self):
        return f"user: {self.username}"

class UserProfile(AbstractBase):
    __tablename__ = "profiles"
    
    bio: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    
    user: Mapped["User"] = relationship("User", back_populates="profile")

class Role(AbstractBase):
    __tablename__ = 'roles'
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    
    permissions: Mapped[list["Permissions"]] = relationship("Permissions", back_populates="roles", secondary="role_permissions")
    users: Mapped[list["User"]] = relationship("User", back_populates="roles", secondary="user_roles")

class Permissions(AbstractBase):
    __tablename__ = 'permissions'
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    
    users: Mapped[list["User"]] = relationship("User", back_populates="permissions", secondary="user_permissions")
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="permissions", secondary="role_permissions")

class SessionModel(AbstractBase):
    __tablename__ = "sessions"
    
    token: Mapped[str] = mapped_column(String, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    user: Mapped["User"] = relationship("User", back_populates="sessions")