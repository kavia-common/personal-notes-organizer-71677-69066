from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from ..models.note_models import Note, NoteCreate, NoteUpdate


@dataclass
class _NoteRecord:
    id: str
    user_id: str
    title: str
    content: str
    tags: Optional[list[str]]
    created_at: datetime
    updated_at: datetime


class NotesService:
    """
    In-memory notes service.
    For demo purposes only. Not persistent, not thread-safe.
    """

    def __init__(self) -> None:
        self._notes: Dict[str, _NoteRecord] = {}  # id -> record
        self._by_user: Dict[str, List[str]] = {}  # user_id -> [note_ids]
        self._counter: int = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"note_{self._counter}"

    # PUBLIC_INTERFACE
    def create_note(self, user_id: str, payload: NoteCreate) -> Note:
        """Create a new note for the user."""
        now = datetime.utcnow()
        note_id = self._next_id()
        rec = _NoteRecord(
            id=note_id,
            user_id=user_id,
            title=payload.title,
            content=payload.content,
            tags=list(payload.tags) if payload.tags is not None else None,
            created_at=now,
            updated_at=now,
        )
        self._notes[note_id] = rec
        self._by_user.setdefault(user_id, []).append(note_id)
        return self._to_model(rec)

    # PUBLIC_INTERFACE
    def list_notes(self, user_id: str) -> List[Note]:
        """List all notes for the user."""
        ids = self._by_user.get(user_id, [])
        return [self._to_model(self._notes[i]) for i in ids]

    # PUBLIC_INTERFACE
    def get_note(self, user_id: str, note_id: str) -> Optional[Note]:
        """Get a single note by id for the user, or None if not found or not owned."""
        rec = self._notes.get(note_id)
        if not rec or rec.user_id != user_id:
            return None
        return self._to_model(rec)

    # PUBLIC_INTERFACE
    def update_note(self, user_id: str, note_id: str, payload: NoteUpdate) -> Optional[Note]:
        """Update fields of an existing note if owned by the user."""
        rec = self._notes.get(note_id)
        if not rec or rec.user_id != user_id:
            return None
        changed = False
        if payload.title is not None:
            rec.title = payload.title
            changed = True
        if payload.content is not None:
            rec.content = payload.content
            changed = True
        if payload.tags is not None:
            rec.tags = list(payload.tags)
            changed = True
        if changed:
            rec.updated_at = datetime.utcnow()
        return self._to_model(rec)

    # PUBLIC_INTERFACE
    def delete_note(self, user_id: str, note_id: str) -> bool:
        """Delete a note if owned by the user. Returns True if deleted."""
        rec = self._notes.get(note_id)
        if not rec or rec.user_id != user_id:
            return False
        del self._notes[note_id]
        user_list = self._by_user.get(user_id, [])
        if note_id in user_list:
            user_list.remove(note_id)
        return True

    def _to_model(self, rec: _NoteRecord) -> Note:
        return Note(
            id=rec.id,
            user_id=rec.user_id,
            title=rec.title,
            content=rec.content,
            tags=list(rec.tags) if rec.tags is not None else None,
            created_at=rec.created_at,
            updated_at=rec.updated_at,
        )


# Singleton service instance for the app lifetime
notes_service = NotesService()
