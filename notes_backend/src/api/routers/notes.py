from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field

from ..core.security import get_current_user_id
from ..models.note_models import Note, NoteCreate, NoteUpdate
from ..services.notes_service import notes_service

router = APIRouter(prefix="/notes", tags=["Notes"])


class DeleteResponse(BaseModel):
    """Response after deleting a note."""
    success: bool = Field(..., description="True if delete succeeded.")
    message: str = Field(..., description="Status message.")


@router.get(
    "",
    summary="List notes",
    response_model=List[Note],
    description="List all notes for the authenticated user.",
)
def list_notes(user_id: str = Depends(get_current_user_id)):
    """
    Returns all notes belonging to the authenticated user.

    Returns:
        List[Note]
    """
    return notes_service.list_notes(user_id)


@router.post(
    "",
    summary="Create note",
    response_model=Note,
    status_code=201,
    description="Create a new note for the authenticated user.",
)
def create_note(payload: NoteCreate, user_id: str = Depends(get_current_user_id)):
    """
    Create a note with validated fields.

    Parameters:
        - payload: NoteCreate containing title, content, and optional tags

    Returns:
        Note: The created note.
    """
    return notes_service.create_note(user_id, payload)


@router.get(
    "/{note_id}",
    summary="Get note",
    response_model=Note,
    responses={404: {"description": "Note not found"}},
    description="Get a note by ID if it belongs to the authenticated user.",
)
def get_note(
    note_id: str = Path(..., description="ID of the note to retrieve"),
    user_id: str = Depends(get_current_user_id),
):
    """
    Retrieve a single note by id.

    Returns:
        Note

    Raises:
        404 if note not found or not owned by user.
    """
    note = notes_service.get_note(user_id, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.patch(
    "/{note_id}",
    summary="Update note",
    response_model=Note,
    responses={404: {"description": "Note not found"}},
    description="Update fields of a note by ID if it belongs to the authenticated user.",
)
def update_note(
    payload: NoteUpdate,
    note_id: str = Path(..., description="ID of the note to update"),
    user_id: str = Depends(get_current_user_id),
):
    """
    Update a note partially.

    Returns:
        Note

    Raises:
        404 if note not found or not owned by user.
    """
    note = notes_service.update_note(user_id, note_id, payload)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.delete(
    "/{note_id}",
    summary="Delete note",
    response_model=DeleteResponse,
    responses={404: {"description": "Note not found"}},
    description="Delete a note by ID if it belongs to the authenticated user.",
)
def delete_note(
    note_id: str = Path(..., description="ID of the note to delete"),
    user_id: str = Depends(get_current_user_id),
):
    """
    Delete a note by id.

    Returns:
        DeleteResponse

    Raises:
        404 if note not found or not owned by user.
    """
    ok = notes_service.delete_note(user_id, note_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return DeleteResponse(success=True, message="Note deleted")
