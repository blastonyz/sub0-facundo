"""Async database helpers compatible with SQLModel.

Provides:
- engine: AsyncEngine built from `DBSettings.sqlalchemy_url` (converted
  to use asyncpg when appropriate)
- AsyncSessionLocal: sessionmaker factory producing AsyncSession
- get_async_session: FastAPI dependency that yields an AsyncSession

This module uses SQLAlchemy's async APIs and is compatible with sqlmodel.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from src.settings.db import DatabaseSettings

# Create async engine
# Use future=True for SQLAlchemy 2.0 style
engine: AsyncEngine = create_async_engine(DatabaseSettings.get_url, future=True)


# Async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an AsyncSession and closes it.

    Usage:
        async def endpoint(db: AsyncSession = Depends(get_async_session)):
            ...
    """

    async with AsyncSessionLocal() as session:
        yield session
