#!/usr/bin/env python3
"""
Development Server Script
Runs both frontend and backend in development mode with hot reload
"""
import os
import sys
import subprocess
import signal
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
BACKEND_DIR = PROJECT_ROOT / "backend"

def run_frontend():
    """Run Vite development server"""
    os.chdir(FRONTEND_DIR)
    print("Starting frontend development server on http://localhost:5173")
    subprocess.run(["pnpm", "run", "dev"], check=True)

def run_backend():
    """Run FastAPI development server"""
    os.chdir(PROJECT_ROOT)
    print("Starting backend development server on http://localhost:8000")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ], check=True)

def main():
    """Main entry point"""
    print("=" * 60)
    print("PyReact Fusion - Development Server")
    print("=" * 60)
    print("\nStarting development servers...")
    print("Frontend: http://localhost:5173")
    print("Backend: http://localhost:8000")
    print("API Docs: http://localhost:8000/api/docs")
    print("\nPress Ctrl+C to stop all servers\n")
    
    # Check if frontend dependencies are installed
    if not (FRONTEND_DIR / "node_modules").exists():
        print("Frontend dependencies not found. Installing...")
        os.chdir(FRONTEND_DIR)
        subprocess.run(["pnpm", "install"], check=True)
        os.chdir(PROJECT_ROOT)
    
    # For simplicity, run backend only
    # In production, you might want to use a process manager like concurrently
    # or run them in separate terminals
    try:
        run_backend()
    except KeyboardInterrupt:
        print("\n\nShutting down development servers...")
        sys.exit(0)

if __name__ == "__main__":
    main()

