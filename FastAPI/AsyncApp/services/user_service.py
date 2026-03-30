from passlib.context import CryptContext
from fastapi import HTTPException, status

from models.user import User
from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate

from passlib.hash import sha256_crypt as pwd_context

# Настройка bcrypt для хэширования паролей
# bcrypt специально медленный — защищает от перебора паролей


class UserService:
    """
    Бизнес логика для работы с пользователями.
    
    Правила которые здесь проверяются:
    - Email должен быть уникальным
    - Пароль хэшируется перед сохранением
    - Неактивные пользователи = "удалённые"
    
    Service НЕ знает про HTTP.
    Он бросает свои ошибки (UserNotFoundError),
    а Router их ловит и превращает в HTTP ответы (404).
    """

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    # ─── Хэширование пароля ───────────────────────────────────

    def _hash_password(self, password: str) -> str:
        """Превратить пароль в хэш. Обратное невозможно."""
        return pwd_context.hash(password)

    def _verify_password(self, plain: str, hashed: str) -> bool:
        """Проверить что пароль совпадает с хэшем."""
        return pwd_context.verify(plain, hashed)

    # ─── Получение ────────────────────────────────────────────

    async def get_user(self, user_id: int) -> User:
        """
        Получить пользователя по ID.
        Бросает UserNotFoundError если не найден или неактивен.
        """
        user = await self.repo.get_by_id(user_id)

        # Неактивные пользователи для нас = не существуют
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

        return user

    async def get_users( self, page: int = 1, page_size: int = 10):
        """Получить страницу пользователей."""
        skip = (page - 1) * page_size  # страница 1 → skip=0, страница 2 → skip=10
        return await self.repo.get_all(skip=skip, limit=page_size)

    # ─── Создание ─────────────────────────────────────────────

    async def create_user(self, data: UserCreate) -> User:
        """
        Создать нового пользователя.
        
        Правила:
        1. Email должен быть уникальным
        2. Сохраняем хэш пароля, а не сам пароль
        3. Email приводим к нижнему регистру
        """
        # Правило 1: проверяем уникальность email
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")

        # Правило 2: хэшируем пароль
        hashed = self._hash_password(data.password)

        # Правило 3: email в нижнем регистре
        new_user = User(
            email=data.email.lower(),
            full_name=data.full_name,
            hashed_password=hashed,
            is_active=True,
        )

        return await self.repo.create(new_user)

    # ─── Обновление ───────────────────────────────────────────

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        """
        Обновить пользователя (только присланные поля).
        
        model_dump(exclude_unset=True) — магия Pydantic!
        Возвращает только поля которые реально прислали.
        
        Если прислали {"full_name": "Новое имя"}:
            updates = {"full_name": "Новое имя"}   ← только это
            is_active не тронем — его не присылали
        """
        user = await self.get_user(user_id)  # проверяем что существует

        updates = data.model_dump(exclude_unset=True)  # только присланные поля

        if not updates:
            return user  # нечего обновлять

        return await self.repo.update(user, updates)

    # ─── Удаление ─────────────────────────────────────────────

    async def delete_user(self, user_id: int) -> None:
        """Мягко удалить пользователя (is_active = False)."""
        user = await self.get_user(user_id)
        await self.repo.soft_delete(user)