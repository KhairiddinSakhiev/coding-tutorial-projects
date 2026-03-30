from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from database.session import get_db
from repositories.user_repository import UserRepository
from schemas.user import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from services.user_service import UserService

# Создаём роутер с префиксом /users
# Все наши эндпоинты будут: /users, /users/{id}, и т.д.
router = APIRouter(
    prefix="/users",
    tags=["Users"],  # группировка в Swagger документации
)


# ─── Dependency Injection ─────────────────────────────────────
# FastAPI сам вызывает эту функцию и передаёт результат в роуты.
# Это называется Dependency Injection (внедрение зависимостей).
# 
# Цепочка: get_db() → UserRepository(db) → UserService(repo)
# Каждый запрос получает свои собственные объекты.

def get_user_service(
    db: AsyncSession = Depends(get_db)  # FastAPI сам передаёт db
) -> UserService:
    """Создаёт сервис для каждого запроса."""
    repo = UserRepository(db)
    return UserService(repo)


# ─── POST /users ── Создать пользователя ─────────────────────

@router.post(
    "/",
    response_model=UserResponse,   # формат ответа
    status_code=status.HTTP_201_CREATED,  # 201 = создано
    summary="Создать пользователя",
)
async def create_user(
    data: UserCreate,  # FastAPI автоматически валидирует входные данные
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Создаёт нового пользователя."""
    try:
        user = await service.create_user(data)
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,  # 409 = конфликт
            detail=str(e),
        )


# ─── GET /users ── Список пользователей ──────────────────────

@router.get("/", response_model=UserListResponse,summary="Список пользователей")
async def list_users(
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    page_size: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    service: UserService = Depends(get_user_service),
) -> UserListResponse:
    """Возвращает список пользователей с пагинацией."""
    users, total = await service.get_users(page=page, page_size=page_size)
    return UserListResponse.create(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
    )


# ─── GET /users/{user_id} ── Один пользователь ───────────────

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя",
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Возвращает одного пользователя по ID."""
    try:
        user = await service.get_user(user_id)
        return UserResponse.model_validate(user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь {user_id} не найден.",
        )


# ─── PATCH /users/{user_id} ── Обновить пользователя ─────────

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Обновить пользователя",
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Частично обновляет пользователя (PATCH).
    
    Присылай только те поля которые хочешь изменить.
    Остальные поля останутся прежними.
    """
    try:
        user = await service.update_user(user_id, data)
        return UserResponse.model_validate(user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь {user_id} не найден.",
        )


# ─── DELETE /users/{user_id} ── Удалить пользователя ─────────

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,  # 204 = удалено, нет тела ответа
    summary="Удалить пользователя",
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> None:
    """Мягко удаляет пользователя (is_active = False)."""
    try:
        await service.delete_user(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь {user_id} не найден.",
        )