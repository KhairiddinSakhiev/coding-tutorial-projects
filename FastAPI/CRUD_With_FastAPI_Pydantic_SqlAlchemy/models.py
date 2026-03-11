from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    username:Mapped[str] = mapped_column(String(100), unique=True)
    password:Mapped[str] = mapped_column(String)
    
    profile:Mapped["UserProfile"] = relationship("UserProfile", back_populates="user")
    tasks:Mapped["Task"] = relationship("Task", back_populates="user")
    user_courses:Mapped["Course"] = relationship("Course", back_populates="users", secondary="user_course")
    
    def __repr__(self):
        return f"user: {self.username}"

class UserProfile(Base):
    __tablename__ = "profiles"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    bio:Mapped[str] = mapped_column(String, nullable=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    
    user:Mapped[User] = relationship(User, back_populates="profile")


class Task(Base):
    __tablename__ = "tasks"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title:Mapped[str] = mapped_column(String, nullable=False)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    
    user:Mapped[User] = relationship(User, back_populates="tasks")


user_course = Table(
    "user_course", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

class Course(Base):
    __tablename__ = "courses"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name:Mapped[str] = mapped_column(String(100))
    
    users:Mapped[User] = relationship(User, back_populates="user_courses", secondary=user_course)
    


"""
user = User.object.filter(id=1).first()
profile = UserProfile.object.filter(user_id=user.id)

"""
