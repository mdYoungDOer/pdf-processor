"""
Vercel serverless entrypoint.
Exposes the NiceGUI PDF Extractor app as an ASGI application at /api.
"""
import sys
from pathlib import Path

# Ensure project root is on path so "main" can be imported
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from main import app  # noqa: E402

# Vercel looks for "app" (ASGI/WSGI) or "handler" (BaseHTTPRequestHandler)
# This file exposes "app" for the Python runtime
