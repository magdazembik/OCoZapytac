
#!/usr/bin/env python3
"""
Main entry point that serves static HTML files and proxies API requests to FastAPI backend
"""
import os
import sys
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.app.main import app
import uvicorn

if __name__ == "__main__":
    # Serve on 0.0.0.0:8000 to make it accessible in Replit
    uvicorn.run(
        app, 
        host="localhost", 
        port=8000
    )
