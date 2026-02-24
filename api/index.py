"""
Vercel serverless entry point.

Re-exports the FastAPI ``app`` from ``api.main`` so that Vercel's Python
runtime can discover and serve it.  Local development still uses
``uvicorn api.main:app --reload``.
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path so that imports like
# ``from config.commodities import COMMODITIES`` resolve correctly
# inside the Vercel serverless environment.
_root = str(Path(__file__).resolve().parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from api.main import app  # noqa: F401
