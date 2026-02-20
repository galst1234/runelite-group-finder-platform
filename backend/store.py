import time
import uuid
from typing import Optional

from models import Activity, CreateGroupRequest, UpdateGroupRequest

TTL_MS = 30 * 60 * 1000  # 30 minutes

_listings: dict[str, dict] = {}


def _now_ms() -> int:
    return int(time.time() * 1000)


def create_listing(req: CreateGroupRequest) -> dict:
    listing_id = str(uuid.uuid4())
    now = _now_ms()
    listing = {
        "id": listing_id,
        "playerName": req.player_name,
        "activity": req.activity.value,
        "currentSize": req.current_size,
        "maxSize": req.max_size,
        "description": req.description,
        "createdAt": now,
        "lastHeartbeat": now,
    }
    _listings[listing_id] = listing
    return listing


def get_listings(activity: Optional[Activity] = None) -> list[dict]:
    cleanup_expired()
    results = list(_listings.values())
    if activity is not None:
        results = [l for l in results if l["activity"] == activity.value]
    return results


def get_listing(listing_id: str) -> Optional[dict]:
    return _listings.get(listing_id)


def delete_listing(listing_id: str) -> bool:
    return _listings.pop(listing_id, None) is not None


def update_listing(listing_id: str, req: UpdateGroupRequest) -> Optional[dict]:
    listing = _listings.get(listing_id)
    if listing is None:
        return None

    if req.current_size is not None:
        listing["currentSize"] = req.current_size
    if req.max_size is not None:
        listing["maxSize"] = req.max_size
    if req.description is not None:
        listing["description"] = req.description

    if listing["currentSize"] > listing["maxSize"]:
        raise ValueError("currentSize must be <= maxSize")

    return listing


def heartbeat(listing_id: str) -> bool:
    listing = _listings.get(listing_id)
    if listing is None:
        return False
    listing["lastHeartbeat"] = _now_ms()
    return True


def cleanup_expired() -> None:
    now = _now_ms()
    expired = [
        lid for lid, listing in _listings.items()
        if now - listing["lastHeartbeat"] > TTL_MS
    ]
    for lid in expired:
        del _listings[lid]
