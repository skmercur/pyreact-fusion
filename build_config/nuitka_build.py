"""
Nuitka Build Configuration
Comprehensive build script for creating standalone executables
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional

class NuitkaBuilder:
    """Nuitka build configuration and execution"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / "backend"
        self.frontend_dir = project_root / "frontend"
        self.build_dir = project_root / "build"
        self.dist_dir = project_root / "dist"
        self.config_dir = project_root / "config"
    
    def build_frontend(self) -> bool:
        """Build React frontend for production"""
        print("Building React frontend...")
        
        if not (self.frontend_dir / "node_modules").exists():
            print("Installing frontend dependencies...")
            os.chdir(self.frontend_dir)
            subprocess.run(["pnpm", "install"], check=True)
        
        os.chdir(self.frontend_dir)
        result = subprocess.run(["pnpm", "run", "build"], check=False)
        
        if result.returncode != 0:
            print("Error: Frontend build failed")
            return False
        
        return (self.frontend_dir / "dist" / "index.html").exists()
    
    def copy_assets(self):
        """Copy frontend assets and config files to backend"""
        print("Copying assets...")
        
        # Copy frontend dist to backend/static
        frontend_dist = self.frontend_dir / "dist"
        backend_static = self.backend_dir / "static"
        
        if backend_static.exists():
            shutil.rmtree(backend_static)
        
        if frontend_dist.exists():
            shutil.copytree(frontend_dist, backend_static)
            print(f"✓ Copied frontend to {backend_static}")
    
    def get_nuitka_command(
        self,
        mode: str = "onefile",
        include_plugins: Optional[List[str]] = None,
        output_name: Optional[str] = None
    ) -> List[str]:
        """Generate Nuitka build command"""
        
        if include_plugins is None:
            include_plugins = ["anti-bloat"]
        
        if output_name is None:
            output_name = "pyreact-fusion"
            if sys.platform == "win32":
                output_name += ".exe"
        
        cmd = [
            sys.executable, "-m", "nuitka",
            "--standalone",
        ]
        
        if mode == "onefile":
            cmd.append("--onefile")
        
        # Plugins
        for plugin in include_plugins:
            cmd.append(f"--enable-plugin={plugin}")
        
        # Include packages
        cmd.extend([
            "--include-package=backend",
            "--include-package=config",
            "--include-package=passlib",
        ])
        
        # Include data directories
        if (self.backend_dir / "static").exists():
            cmd.append(f"--include-data-dir={self.backend_dir / 'static'}=backend/static")
        
        if self.config_dir.exists():
            cmd.append(f"--include-data-dir={self.config_dir}=config")
        
        # Database drivers
        cmd.extend([
            "--include-module=psycopg2",
            "--include-module=pymysql",
            "--include-module=pymongo",
        ])
        
        # Output configuration
        cmd.extend([
            f"--output-dir={self.dist_dir}",
            f"--output-filename={output_name}",
        ])
        
        # Platform-specific options
        if sys.platform == "win32":
            cmd.append("--windows-console-mode=hide")
        elif sys.platform == "darwin":
            cmd.append("--macos-create-app-bundle")
        
        # Main module
        cmd.append("backend/main.py")
        
        return cmd
    
    def build(
        self,
        mode: str = "onefile",
        build_frontend: bool = True,
        output_name: Optional[str] = None
    ) -> bool:
        """Execute complete build process"""
        print("=" * 60)
        print("Nuitka Build Process")
        print("=" * 60)
        
        try:
            # Step 1: Build frontend
            if build_frontend:
                if not self.build_frontend():
                    return False
                self.copy_assets()
            
            # Step 2: Build with Nuitka
            print("\nBuilding executable with Nuitka...")
            os.chdir(self.project_root)
            
            cmd = self.get_nuitka_command(mode=mode, output_name=output_name)
            print(f"Command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, check=False)
            
            if result.returncode != 0:
                print("Error: Nuitka build failed")
                return False
            
            print("\n✓ Build complete!")
            print(f"Executable: {self.dist_dir / (output_name or 'pyreact-fusion')}")
            
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False


def main():
    """Main entry point"""
    project_root = Path(__file__).parent.parent
    builder = NuitkaBuilder(project_root)
    
    # Parse command line arguments
    mode = "onefile"
    if len(sys.argv) > 1:
        mode = sys.argv[1]  # "onefile" or "standalone"
    
    success = builder.build(mode=mode)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

