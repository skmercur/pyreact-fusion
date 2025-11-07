#!/usr/bin/env python3
"""
Frontend Build Script
Builds the React application for production
"""
import os
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def main():
    """Build the frontend application"""
    print("=" * 60)
    print("Building React Frontend")
    print("=" * 60)
    
    # Check if frontend directory exists
    if not FRONTEND_DIR.exists():
        print(f"Error: Frontend directory not found at {FRONTEND_DIR}")
        sys.exit(1)
    
    # Check if node_modules exists
    if not (FRONTEND_DIR / "node_modules").exists():
        print("Installing frontend dependencies...")
        os.chdir(FRONTEND_DIR)
        result = subprocess.run(["pnpm", "install"], check=False)
        if result.returncode != 0:
            print("Error: Failed to install frontend dependencies")
            sys.exit(1)
    
    # Build the frontend
    print("\nBuilding production bundle...")
    os.chdir(FRONTEND_DIR)
    result = subprocess.run(["pnpm", "run", "build"], check=False)
    
    if result.returncode != 0:
        print("Error: Frontend build failed")
        sys.exit(1)
    
    # Check if build was successful
    dist_dir = FRONTEND_DIR / "dist"
    if dist_dir.exists() and (dist_dir / "index.html").exists():
        print(f"\n[OK] Frontend build successful!")
        print(f"  Build output: {dist_dir}")
        print(f"  Size: {sum(f.stat().st_size for f in dist_dir.rglob('*') if f.is_file()) / 1024:.2f} KB")
    else:
        print("Error: Build output not found")
        sys.exit(1)

if __name__ == "__main__":
    main()

