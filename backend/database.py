from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_async_engine(DATABASE_URL)
_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    # Connection is validated lazily on first use; nothing to do here.
    pass


async def close_db() -> None:
    await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with _session_factory() as session:
        yield session
