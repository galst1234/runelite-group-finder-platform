import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Activity(StrEnum):
    CHAMBERS_OF_XERIC = "CHAMBERS_OF_XERIC"
    THEATRE_OF_BLOOD = "THEATRE_OF_BLOOD"
    TOMBS_OF_AMASCUT = "TOMBS_OF_AMASCUT"
    GENERAL_GRAARDOR = "GENERAL_GRAARDOR"
    COMMANDER_ZILYANA = "COMMANDER_ZILYANA"
    KRIL_TSUTSAROTH = "KRIL_TSUTSAROTH"
    KREEARRA = "KREEARRA"
    NEX = "NEX"
    NIGHTMARE = "NIGHTMARE"
    CORPOREAL_BEAST = "CORPOREAL_BEAST"
    HUEYCOATL = "HUEYCOATL"
    ROYAL_TITANS = "ROYAL_TITANS"
    BARBARIAN_ASSAULT = "BARBARIAN_ASSAULT"
    OTHER = "OTHER"


class CreateGroupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    player_name: str = Field(alias="playerName", min_length=1, max_length=12)
    activity: Activity
    current_size: int = Field(alias="currentSize", ge=1, le=100)
    max_size: int = Field(alias="maxSize", ge=2, le=100)
    description: str = Field(default="", max_length=200)
    friends_chat_name: str = Field(default="", alias="friendsChatName", max_length=12)

    @model_validator(mode="after")
    def current_size_le_max_size(self) -> Self:
        if self.current_size > self.max_size:
            raise ValueError("currentSize must be <= maxSize")
        return self


class UpdateGroupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    current_size: int | None = Field(None, alias="currentSize", ge=1, le=100)
    max_size: int | None = Field(None, alias="maxSize", ge=2, le=100)
    description: str | None = Field(None, max_length=200)


class GroupListingResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True, from_attributes=True)

    id: str
    player_name: str = Field(alias="playerName")
    activity: Activity
    current_size: int = Field(alias="currentSize")
    max_size: int = Field(alias="maxSize")
    description: str
    friends_chat_name: str = Field(alias="friendsChatName")
    created_at: datetime.datetime = Field(alias="createdAt")
