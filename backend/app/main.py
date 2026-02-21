import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession

from app import store
from app.database import close_db, engine, init_db
from app.routes import router


async def _cleanup_loop() -> None:
    while True:
        await asyncio.sleep(60)
        async with AsyncSession(engine) as session:
            await store.cleanup_expired(session)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    await init_db()
    task = asyncio.create_task(_cleanup_loop())
    yield
    task.cancel()
    await close_db()


app = FastAPI(title="RuneLite Group Finder", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,  # ty: ignore[invalid-argument-type]  # ParamSpec limitation
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
