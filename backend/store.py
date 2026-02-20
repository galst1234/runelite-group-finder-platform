import time
import uuid
from typing import Optional

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Activity, CreateGroupRequest, GroupListing, UpdateGroupRequest

TTL_MS = 30 * 60 * 1000  # 30 minutes


def _now_ms() -> int:
    return int(time.time() * 1000)


async def create_listing(session: AsyncSession, req: CreateGroupRequest) -> GroupListing:
    now = _now_ms()
    listing = GroupListing(
        id=str(uuid.uuid4()),
        player_name=req.player_name,
        activity=req.activity.value,
        current_size=req.current_size,
        max_size=req.max_size,
        description=req.description,
        created_at=now,
        last_heartbeat=now,
    )
    session.add(listing)
    await session.commit()
    await session.refresh(listing)
    return listing


async def get_listings(session: AsyncSession, activity: Optional[Activity] = None) -> list[GroupListing]:
    statement = select(GroupListing)
    if activity is not None:
        statement = statement.where(GroupListing.activity == activity.value)
    result = await session.exec(statement)
    return list(result.all())


async def get_listing(session: AsyncSession, listing_id: str) -> Optional[GroupListing]:
    return await session.get(GroupListing, listing_id)


async def delete_listing(session: AsyncSession, listing_id: str) -> bool:
    listing = await session.get(GroupListing, listing_id)
    if listing is None:
        return False
    await session.delete(listing)
    await session.commit()
    return True


async def update_listing(session: AsyncSession, listing_id: str, req: UpdateGroupRequest) -> Optional[GroupListing]:
    listing = await session.get(GroupListing, listing_id)
    if listing is None:
        return None

    if req.current_size is not None:
        listing.current_size = req.current_size
    if req.max_size is not None:
        listing.max_size = req.max_size
    if req.description is not None:
        listing.description = req.description

    if listing.current_size > listing.max_size:
        raise ValueError("currentSize must be <= maxSize")

    await session.commit()
    await session.refresh(listing)
    return listing


async def heartbeat(session: AsyncSession, listing_id: str) -> bool:
    listing = await session.get(GroupListing, listing_id)
    if listing is None:
        return False
    listing.last_heartbeat = _now_ms()
    await session.commit()
    return True


async def cleanup_expired(session: AsyncSession) -> None:
    cutoff = _now_ms() - TTL_MS
    await session.exec(delete(GroupListing).where(GroupListing.last_heartbeat < cutoff))
    await session.commit()
