from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi as _get_openapi

OPENAPI_TAGS = [
    {
        "name": "Health",
        "description": "System health endpoints.",
    },
    {
        "name": "Auth",
        "description": "Register and login to obtain tokens.",
    },
    {
        "name": "Notes",
        "description": "Create, read, update, and delete personal notes.",
    },
]


def get_openapi_schema(app: FastAPI):
    """
    Generate and cache the OpenAPI schema for the app with custom tags and metadata.

    Args:
        app: The FastAPI application.

    Returns:
        dict: The OpenAPI schema.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = _get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
