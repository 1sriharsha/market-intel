"""FastAPI dependencies — DB session, shared clients."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from storage.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
