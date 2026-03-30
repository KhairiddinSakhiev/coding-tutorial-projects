import math
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ─── Схема для создания пользователя ─────────────────────────
class UserCreate(BaseModel):
    """Данные которые нужно прислать чтобы создать пользователя."""
    
    email: EmailStr  # pydantic проверит что это валидный email
    
    full_name: str = Field(
        min_length=2,    # минимум 2 символа
        max_length=200,  # максимум 200 символов
        examples=["Алибек Каримов"],
    )
    
    password: str = Field(
        min_length=8,    # минимум 8 символов
        examples=["MyPass123!"],
    )


# ─── Схема для обновления пользователя ───────────────────────
class UserUpdate(BaseModel):
    """
    Данные для обновления пользователя.
    
    Все поля Optional потому что PATCH = обновляем только то что прислали.
    Если прислали только full_name — меняем только full_name.
    """
    
    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=200,
    )
    
    is_active: Optional[bool] = None


# ─── Схема ответа ─────────────────────────────────────────────
class UserResponse(BaseModel):
    """
    Данные которые мы отправляем пользователю в ответ.
    
    ВАЖНО: hashed_password здесь нет!
    Никогда не показываем хэш пароля через API.
    
    from_attributes=True позволяет pydantic читать данные
    из SQLAlchemy объектов (не только из словарей).
    """
    
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Схема для списка пользователей ──────────────────────────
class UserListResponse(BaseModel):
    """Ответ со списком пользователей и информацией о страницах."""
    
    items: list[UserResponse]
    total: int       # всего пользователей в БД
    page: int        # текущая страница
    page_size: int   # пользователей на странице
    pages: int       # всего страниц

    @classmethod
    def create(cls, items, total, page, page_size):
        """Создаёт объект и автоматически считает количество страниц."""
        pages = math.ceil(total / page_size) if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )