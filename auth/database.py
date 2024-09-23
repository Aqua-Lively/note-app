from typing import AsyncGenerator, List

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship
from sqlalchemy import Boolean, String, Integer, TIMESTAMP, ForeignKey
from datetime import datetime

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):

        id: Mapped[int] = mapped_column(Integer, primary_key=True)
        email: Mapped[str] = mapped_column(String, nullable=False)
        username: Mapped[str] = mapped_column(String, nullable=False)
        registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
        hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
        is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
        is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
        note: Mapped[List['Note']] = relationship(back_populates='user')

class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='note')

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)