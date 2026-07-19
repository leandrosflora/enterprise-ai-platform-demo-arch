from __future__ import annotations

try:
    from .main import app
    from .rag_memory_security import router
except ImportError:  # Docker executes modules directly from /app
    from main import app  # type: ignore
    from rag_memory_security import router  # type: ignore

app.include_router(router)
