import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

import store
from database import close_db, engine, init_db
from routes import router


async def _cleanup_loop():
    while True:
        await asyncio.sleep(60)
        async with AsyncSession(engine) as session:
            await store.cleanup_expired(session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    task = asyncio.create_task(_cleanup_loop())
    yield
    task.cancel()
    await close_db()


app = FastAPI(title="RuneLite Group Finder", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
