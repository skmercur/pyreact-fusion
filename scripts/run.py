#!/usr/bin/env python3
"""
Application Runner
Runs the application in the selected mode (Desktop or Web)
"""
import os
import sys
import json
import webbrowser
import threading
from pathlib import Path
from rich.console import Console

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CONFIG_FILE = PROJECT_ROOT / "app_config.json"
console = Console()


def load_config():
    """Load application configuration"""
    if not CONFIG_FILE.exists():
        console.print("[yellow]Configuration file not found![/yellow]")
        console.print("[cyan]Running initial setup...[/cyan]\n")
        
        # Run setup automatically using subprocess
        import subprocess
        import sys
        subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "setup.py")])
        
        # Reload config after setup
        if not CONFIG_FILE.exists():
            console.print("[red]Setup failed. Please run setup manually:[/red]")
            console.print("[cyan]  python scripts/setup.py[/cyan]\n")
            sys.exit(1)
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def run_web_mode(config):
    """Run application in web mode (browser)"""
    server = config.get("server", {})
    host = server.get("host", "0.0.0.0")
    port = server.get("port", 8000)
    
    # For browser access, use localhost (0.0.0.0 is for binding only)
    browser_url = f"http://localhost:{port}"
    
    console.print(f"[green]Starting server on {host}:{port}...[/green]")
    console.print(f"[green]Access at: {browser_url}[/green]")
    
    # Ensure project root is in path
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    
    # Check if frontend is built
    frontend_dist = PROJECT_ROOT / "frontend" / "dist"
    if not frontend_dist.exists() or not (frontend_dist / "index.html").exists():
        console.print("[yellow]Frontend not built. Building now...[/yellow]")
        import subprocess
        build_result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "build_frontend.py")],
            cwd=str(PROJECT_ROOT),
            capture_output=True
        )
        if build_result.returncode != 0:
            console.print("[red]Frontend build failed![/red]")
            console.print("[yellow]Please build frontend manually: python scripts/build_frontend.py[/yellow]")
        else:
            console.print("[green]✓ Frontend built successfully[/green]")
    
    # Start the server
    import uvicorn
    from backend.config import settings
    
    # Update settings from config
    settings.host = host
    settings.port = port
    
    # Open browser after a short delay
    def open_browser():
        import time
        time.sleep(2)
        try:
            webbrowser.open(browser_url)
            console.print(f"[green]✓ Browser opened at {browser_url}[/green]\n")
        except Exception as e:
            console.print(f"[yellow]Could not open browser automatically: {e}[/yellow]")
            console.print(f"[cyan]Please open manually: {browser_url}[/cyan]\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run server
    from backend.main import app
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


def run_desktop_mode(config):
    """Run application in desktop mode (pywebview)"""
    try:
        import webview
    except ImportError:
        console.print("[red]pywebview is not installed![/red]")
        console.print("[yellow]Install it with:[/yellow]")
        console.print("[cyan]  pip install pywebview[/cyan]\n")
        sys.exit(1)
    
    server = config.get("server", {})
    # For desktop mode, always use 127.0.0.1 (pywebview needs specific IP)
    # Server binds to 127.0.0.1, URL also uses 127.0.0.1
    bind_host = "127.0.0.1"
    port = server.get("port", 8000)
    
    url = f"http://127.0.0.1:{port}"
    app_name = config.get("app", {}).get("name", "PyReact Fusion")
    
    console.print(f"[green]Starting server on {url}...[/green]")
    console.print(f"[green]Opening desktop window: {app_name}[/green]")
    console.print("[dim]Close the window to stop the application[/dim]\n")
    
    # Check if frontend is built
    frontend_dist = PROJECT_ROOT / "frontend" / "dist"
    if not frontend_dist.exists() or not (frontend_dist / "index.html").exists():
        console.print("[yellow]Frontend not built. Building now...[/yellow]")
        import subprocess
        build_result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "build_frontend.py")],
            cwd=str(PROJECT_ROOT),
            capture_output=True
        )
        if build_result.returncode != 0:
            console.print("[red]Frontend build failed![/red]")
            console.print("[yellow]Please build frontend manually: python scripts/build_frontend.py[/yellow]")
        else:
            console.print("[green]✓ Frontend built successfully[/green]")
    
    # Start server in background thread
    def start_server():
        # Ensure project root is in path
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))
        
        import uvicorn
        from backend.config import settings
        
        # Use 127.0.0.1 for desktop mode (pywebview requirement)
        settings.host = bind_host
        settings.port = port
        
        from backend.main import app
        uvicorn.run(
            app,
            host=bind_host,
            port=port,
            log_level="warning"  # Reduce console output
        )
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait a bit for server to start
    import time
    time.sleep(2)
    
    # Create and show window
    try:
        webview.create_window(
            app_name,
            url,
            width=1200,
            height=800,
            min_size=(800, 600),
            resizable=True
        )
        
        webview.start(debug=False)
    except Exception as e:
        console.print(f"[red]Error creating desktop window: {e}[/red]")
        console.print("[yellow]Falling back to web mode...[/yellow]\n")
        run_web_mode(config)


def main():
    """Main entry point"""
    console.print("\n[bold cyan]PyReact Fusion[/bold cyan] - Starting Application\n")
    
    # Load configuration
    config = load_config()
    
    # Display configuration info
    app_info = config.get("app", {})
    app_name = app_info.get("name", "PyReact Fusion")
    mode = config.get("mode", "web")
    server = config.get("server", {})
    port = server.get("port", 8000)
    
    console.print(f"[green]App:[/green] {app_name}")
    console.print(f"[green]Mode:[/green] {mode.title()}")
    console.print(f"[green]Port:[/green] {port}\n")
    
    # Run in selected mode
    if mode == "desktop":
        run_desktop_mode(config)
    else:
        run_web_mode(config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Application stopped.[/yellow]\n")
        sys.exit(0)

