from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, notes
from .core.openapi import get_openapi_schema, OPENAPI_TAGS


def create_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI app with CORS, routes, and OpenAPI metadata.
    """
    app = FastAPI(
        title="Personal Notes Backend",
        description=(
            "A simple backend service for managing personal notes.\n\n"
            "Features:\n"
            "- Token-based auth (mocked, non-persistent)\n"
            "- CRUD for notes scoped to the authenticated user\n"
            "- Pydantic validation and OpenAPI docs\n"
        ),
        version="0.1.0",
        contact={"name": "Notes Backend", "url": "https://example.com"},
        openapi_tags=OPENAPI_TAGS,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check
    @app.get("/", tags=["Health"], summary="Health Check", description="Simple health check endpoint.")
    def health_check():
        return {"message": "Healthy"}

    # Routers
    app.include_router(auth.router)
    app.include_router(notes.router)

    # Custom OpenAPI generation to include websocket notes in docs (if added later)
    app.openapi = lambda: get_openapi_schema(app)

    return app


# Create ASGI app instance
app = create_app()
