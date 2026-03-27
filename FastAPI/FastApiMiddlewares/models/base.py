from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer

class Base(DeclarativeBase):
    pass

class AbstractBase(Base):
    __abstract__ = True
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)