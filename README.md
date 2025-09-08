# personal-notes-organizer-71677-69066

Backend: FastAPI service for personal notes.

How to run locally:
- Ensure Python 3.11+ and pip are available.
- Install dependencies:
  pip install -r notes_backend/requirements.txt
- Run with uvicorn:
  uvicorn notes_backend.src.api.main:app --reload

Auth:
- Register: POST /auth/register { "email": "you@example.com", "password": "yourpass" }
- Login: POST /auth/login { "email": "you@example.com", "password": "yourpass" }
- Use Authorization: Bearer <token> header for all /notes endpoints.

Notes:
- GET /notes
- POST /notes
- GET /notes/{note_id}
- PATCH /notes/{note_id}
- DELETE /notes/{note_id}

This implementation uses in-memory storage and a mock token store for simplicity (non-persistent).
