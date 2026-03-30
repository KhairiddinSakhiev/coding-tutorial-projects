from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.session import Base


class User(Base):
    """
    Модель пользователя = таблица 'users' в базе данных.
    
    Каждый атрибут = колонка в таблице.
    """
    
    __tablename__ = "users"  # имя таблицы в PostgreSQL

    # id — первичный ключ, автоматически увеличивается (1, 2, 3...)
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # email — уникальный, с индексом для быстрого поиска
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,     # два пользователя не могут иметь одинаковый email
        nullable=False,  # обязательное поле
        index=True,      # индекс = быстрый поиск по email
    )

    full_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    # НИКОГДА не храним пароль в открытом виде — только хэш!
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # is_active — мягкое удаление (не удаляем, а деактивируем)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Время создания — ставит база данных, не Python
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # БД ставит время при создании
    )

    # Время обновления — автоматически меняется при каждом UPDATE
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),        # БД обновляет время при изменении
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"