import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from .models import Base, User, Bonus

# Настройки подключения к базе данных
DB_URL = "sqlite+aiosqlite:///database.db"

async_engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_db():
    """Контекстный менеджер для получения сессии БД."""
    async with AsyncSessionLocal() as db_session:
        yield db_session

async def is_user_in_database(id: int, session: AsyncSession) -> bool:
    """Проверяет, есть ли пользователь с указанным tg_id в базе данных."""
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user is not None


async def get_or_create_bonus(user_id: int, session: AsyncSession) -> Bonus:
    query = select(Bonus).where(Bonus.user_id == user_id)
    result = await session.execute(query)
    bonus = result.scalar_one_or_none()
    if bonus is None:
        new_bonus = Bonus(user_id=user_id)
        session.add(new_bonus)
        await session.commit()
        return new_bonus
    return bonus

async def update_coffees_count(user_id: int, session: AsyncSession, increment: int = 1):
    """ Обновляет количество купленных чашек кофе для пользователя. :param user_id: Идентификатор пользователя. :param increment: Количество чашек кофе для прибавления. :param session: Сессия БД. """
    bonus = await get_or_create_bonus(user_id, session)
    bonus.coffees_count += increment
    await session.commit()

async def check_for_free_coffee(user_id: int, session: AsyncSession) -> bool:
    """ Проверяет, достиг ли пользователь права на бесплатную чашку кофе. :param user_id: Идентификатор пользователя. :param session: Сессия БД. :return: True, если пользователь имеет право на бесплатную чашку кофе, иначе False. """
    bonus = await get_or_create_bonus(user_id, session)
    if bonus.coffees_count >= 6:
        bonus.coffees_count -= 6
        await session.commit()
        return True
    return False



async def is_admin(user_id: int) -> bool:
    async with AsyncSessionMaker() as session:
        result = await session.execute(select(Admin).where(Admin.telegram_id == user_id))
        admin = result.scalar_one_or_none()
        return admin is not None
async def init_db():
    """Инициализация базы данных и создание всех таблиц."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

