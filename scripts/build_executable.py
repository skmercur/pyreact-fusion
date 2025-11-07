#!/usr/bin/env python3
"""
Complete Build Pipeline Script
Builds frontend and compiles backend to executable using Nuitka
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
BACKEND_DIR = PROJECT_ROOT / "backend"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"

def build_frontend():
    """Build the React frontend"""
    print("\n" + "=" * 60)
    print("Step 1: Building Frontend")
    print("=" * 60)
    
    if not (FRONTEND_DIR / "node_modules").exists():
        print("Installing frontend dependencies...")
        os.chdir(FRONTEND_DIR)
        subprocess.run(["pnpm", "install"], check=True)
    
    print("Building React app...")
    os.chdir(FRONTEND_DIR)
    subprocess.run(["pnpm", "run", "build"], check=True)
    
    if not (FRONTEND_DIR / "dist" / "index.html").exists():
        raise Exception("Frontend build failed - index.html not found")
    
    print("✓ Frontend build complete")

def copy_frontend_to_backend():
    """Copy built frontend to backend static directory"""
    print("\n" + "=" * 60)
    print("Step 2: Copying Frontend Assets")
    print("=" * 60)
    
    frontend_dist = FRONTEND_DIR / "dist"
    backend_static = BACKEND_DIR / "static"
    
    if backend_static.exists():
        shutil.rmtree(backend_static)
    
    shutil.copytree(frontend_dist, backend_static)
    print(f"✓ Copied frontend assets to {backend_static}")

def build_with_nuitka():
    """Build executable using Nuitka"""
    print("\n" + "=" * 60)
    print("Step 3: Building Executable with Nuitka")
    print("=" * 60)
    
    os.chdir(PROJECT_ROOT)
    
    # Determine output filename based on platform
    if sys.platform == "win32":
        output_name = "pyreact-fusion.exe"
    else:
        output_name = "pyreact-fusion"
    
    # Nuitka build command
    nuitka_cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=anti-bloat",
        "--include-package=backend",
        "--include-package=config",
        "--include-data-dir=backend/static=backend/static",
        "--include-data-dir=config=config",
        "--output-dir=dist",
        f"--output-filename={output_name}",
        "backend/main.py"  # Only one positional argument - the main module
    ]
    
    # Platform-specific adjustments
    if sys.platform == "win32":
        # Windows: Hide console window (for desktop app)
        nuitka_cmd.append("--windows-console-mode=hide")
    elif sys.platform == "darwin":
        nuitka_cmd.append("--macos-create-app-bundle")
    
    print("Running Nuitka...")
    print(f"Command: {' '.join(nuitka_cmd)}")
    
    result = subprocess.run(nuitka_cmd, check=False)
    
    if result.returncode != 0:
        print("Error: Nuitka build failed")
        sys.exit(1)
    
    print("✓ Executable build complete")

def main():
    """Main build pipeline"""
    print("=" * 60)
    print("PyReact Fusion - Complete Build Pipeline")
    print("=" * 60)
    
    try:
        # Step 1: Build frontend
        build_frontend()
        
        # Step 2: Copy frontend to backend
        copy_frontend_to_backend()
        
        # Step 3: Build executable
        build_with_nuitka()
        
        print("\n" + "=" * 60)
        print("Build Complete!")
        print("=" * 60)
        print(f"\nExecutable location: {DIST_DIR}")
        print("\nTo run the application:")
        if sys.platform == "win32":
            print("  dist\\pyreact-fusion.exe")
        else:
            print("  dist/pyreact-fusion")
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

