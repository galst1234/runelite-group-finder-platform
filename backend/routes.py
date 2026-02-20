from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession

import store
from database import get_session
from models import (
    Activity,
    CreateGroupRequest,
    GroupListingResponse,
    UpdateGroupRequest,
)

router = APIRouter(prefix="/api/groups")


@router.get("", response_model=list[GroupListingResponse])
async def list_groups(activity: Activity | None = None, session: AsyncSession = Depends(get_session)):
    return await store.get_listings(session, activity)


@router.post("", response_model=GroupListingResponse, status_code=201)
async def create_group(req: CreateGroupRequest, session: AsyncSession = Depends(get_session)):
    return await store.create_listing(session, req)


@router.delete("/{listing_id}", status_code=204)
async def delete_group(listing_id: str, session: AsyncSession = Depends(get_session)):
    if not await store.delete_listing(session, listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")
    return Response(status_code=204)


@router.patch("/{listing_id}", response_model=GroupListingResponse)
async def update_group(listing_id: str, req: UpdateGroupRequest, session: AsyncSession = Depends(get_session)):
    try:
        listing = await store.update_listing(session, listing_id, req)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.post("/{listing_id}/heartbeat")
async def heartbeat(listing_id: str, session: AsyncSession = Depends(get_session)):
    if not await store.heartbeat(session, listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"status": "ok"}
