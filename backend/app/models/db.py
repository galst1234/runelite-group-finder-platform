import uuid

from sqlmodel import Field, SQLModel


class GroupListing(SQLModel, table=True):
    __tablename__ = "group_listings"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    player_name: str = Field(max_length=12)
    activity: str = Field(max_length=50)
    current_size: int
    max_size: int
    description: str = Field(default="", max_length=200)
    created_at: int
    last_heartbeat: int
