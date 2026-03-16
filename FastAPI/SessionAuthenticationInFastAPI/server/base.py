from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, DateTime
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class AbstractBase(Base):
    __abstract__ = True
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
