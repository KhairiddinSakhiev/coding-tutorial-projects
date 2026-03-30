from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.user import User


class UserRepository:
    def __init__(self, db:AsyncSession):
        self.db = db
        
        
    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Найти пользователя по email (без учёта регистра)."""
        result = await self.db.execute(
            select(User).where(
                func.lower(User.email) == email.lower()
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 10):
        """
        Получить список активных пользователей с пагинацией.
        
        Возвращает: (список пользователей, общее количество)
        
        skip — сколько пропустить (для пагинации)
        limit — сколько взять (размер страницы)
        """
        # Считаем общее количество активных пользователей
        count_result = await self.db.execute(
            select(func.count())
            .select_from(User)
            .where(User.is_active.is_(True))
        )
        total = count_result.scalar_one()

        # Получаем страницу пользователей
        items_result = await self.db.execute(
            select(User)
            .where(User.is_active.is_(True))
            .order_by(User.id)  # сортировка по ID
            .offset(skip)       # пропускаем первые skip записей
            .limit(limit)       # берём только limit записей
        )
        items = list(items_result.scalars().all())

        return items, total

    # ─── Создание ─────────────────────────────────────────────

    async def create(self, user: User) -> User:
        """
        Сохранить нового пользователя в базу данных.
        
        db.add()    — регистрируем объект (ещё не в БД)
        db.flush()  — отправляем INSERT, получаем ID от БД
        db.refresh() — перечитываем объект (получаем id, created_at)
        """
        self.db.add(user)
        await self.db.flush()         # отправляем INSERT в БД
        await self.db.refresh(user)   # получаем id и timestamps
        return user

    # ─── Обновление ───────────────────────────────────────────

    async def update(self, user: User, updates: dict) -> User:
        """
        Обновить поля пользователя.
        
        updates — словарь с полями которые нужно изменить.
        Поля которых нет в словаре — не трогаем.
        """
        for field, value in updates.items():
            setattr(user, field, value)  # меняем атрибут объекта

        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    # ─── Удаление ─────────────────────────────────────────────

    async def soft_delete(self, user: User) -> None:
        """
        Мягкое удаление — is_active = False.
        
        Мы НЕ удаляем строку из базы данных.
        Это сохраняет историю и связи с другими таблицами.
        Пользователь просто перестаёт появляться в результатах.
        """
        user.is_active = False
        self.db.add(user)
        await self.db.flush()