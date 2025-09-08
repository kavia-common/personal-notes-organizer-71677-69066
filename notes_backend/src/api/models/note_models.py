from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class NoteBase(BaseModel):
    """Base note properties with validation."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the note.")
    content: str = Field(..., min_length=1, description="Content/body of the note.")
    tags: Optional[list[str]] = Field(default=None, description="List of tags for categorization.")

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]):
        if v is None:
            return v
        if len(v) > 25:
            raise ValueError("Too many tags (max 25).")
        for t in v:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("Tags must be non-empty strings.")
            if len(t) > 40:
                raise ValueError("Individual tag length must be <= 40.")
        return [t.strip() for t in v]


class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note with partial fields."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Updated title.")
    content: Optional[str] = Field(default=None, min_length=1, description="Updated content.")
    tags: Optional[list[str]] = Field(default=None, description="Updated tags list.")

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: Optional[list[str]]):
        if v is None:
            return v
        if len(v) > 25:
            raise ValueError("Too many tags (max 25).")
        for t in v:
            if not isinstance(t, str) or not t.strip():
                raise ValueError("Tags must be non-empty strings.")
            if len(t) > 40:
                raise ValueError("Individual tag length must be <= 40.")
        return [t.strip() for t in v]


class Note(NoteBase):
    """Note model returned by the API."""
    id: str = Field(..., description="Unique identifier for the note.")
    user_id: str = Field(..., description="Owner user identifier.")
    created_at: datetime = Field(..., description="Creation timestamp.")
    updated_at: datetime = Field(..., description="Last updated timestamp.")
