"""Pydantic models for PromptLab"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


def generate_id() -> str:
    return str(uuid4())


def get_current_time() -> datetime:
    return datetime.now(timezone.utc)


# ============== Prompt Models ==============


class PromptBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: str | None = Field(None, max_length=500)
    collection_id: str | None = None
    tags: list[str] = Field(default_factory=list, max_items=50)


class PromptCreate(PromptBase):
    pass


class PromptUpdate(PromptBase):
    pass


class PromptPatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)
    description: str | None = Field(None, max_length=500)
    collection_id: str | None = None
    tags: list[str] | None = Field(default=None, max_items=50)


class Prompt(PromptBase):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============


class CollectionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============


class PromptList(BaseModel):
    prompts: list[Prompt]
    total: int


class CollectionList(BaseModel):
    collections: list[Collection]
    total: int


class HealthResponse(BaseModel):
    status: str
    version: str
