from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app import store
from app.database import get_session
from app.models.api import (
    Activity,
    CreateGroupRequest,
    GroupListingResponse,
    UpdateGroupRequest,
)

router = APIRouter(prefix="/api/groups")


@router.get("")
async def list_groups(
    session: Annotated[AsyncSession, Depends(get_session)],
    activity: Activity | None = None,
) -> list[GroupListingResponse]:
    listings = await store.get_listings(session, activity)
    return [GroupListingResponse.model_validate(listing) for listing in listings]


@router.post("", status_code=201)
async def create_group(
    req: CreateGroupRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> GroupListingResponse:
    listing = await store.create_listing(session, req)
    return GroupListingResponse.model_validate(listing)


@router.delete("/{listing_id}", status_code=204)
async def delete_group(listing_id: str, session: Annotated[AsyncSession, Depends(get_session)]) -> Response:
    if not await store.delete_listing(session, listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")
    return Response(status_code=204)


@router.patch("/{listing_id}")
async def update_group(
    listing_id: str,
    req: UpdateGroupRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> GroupListingResponse:
    try:
        listing = await store.update_listing(session, listing_id, req)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return GroupListingResponse.model_validate(listing)


@router.post("/{listing_id}/heartbeat")
async def heartbeat(listing_id: str, session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, str]:
    if not await store.heartbeat(session, listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"status": "ok"}
