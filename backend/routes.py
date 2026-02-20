from typing import Optional

from fastapi import APIRouter, HTTPException, Response

import store
from models import (
    Activity,
    CreateGroupRequest,
    GroupListingResponse,
    UpdateGroupRequest,
)

router = APIRouter(prefix="/api/groups")


@router.get("", response_model=list[GroupListingResponse])
async def list_groups(activity: Optional[Activity] = None):
    return store.get_listings(activity)


@router.post("", response_model=GroupListingResponse, status_code=201)
async def create_group(req: CreateGroupRequest):
    return store.create_listing(req)


@router.delete("/{listing_id}", status_code=204)
async def delete_group(listing_id: str):
    if not store.delete_listing(listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")
    return Response(status_code=204)


@router.patch("/{listing_id}", response_model=GroupListingResponse)
async def update_group(listing_id: str, req: UpdateGroupRequest):
    try:
        listing = store.update_listing(listing_id, req)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.post("/{listing_id}/heartbeat")
async def heartbeat(listing_id: str):
    if not store.heartbeat(listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"status": "ok"}
