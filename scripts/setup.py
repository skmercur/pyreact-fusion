#!/usr/bin/env python3
"""
Initial Setup TUI
Interactive setup for PyReact Fusion application
"""
import os
import sys
import json
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box

console = Console()

CONFIG_FILE = PROJECT_ROOT / "app_config.json"


def print_header():
    """Print welcome header"""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]PyReact Fusion[/bold cyan] - Application Setup",
        border_style="cyan",
        box=box.DOUBLE
    ))
    console.print()


def get_app_mode():
    """Get application mode (Desktop or Web)"""
    console.print("[bold yellow]Step 1: Choose Application Mode[/bold yellow]\n")
    console.print("How would you like to run your application?")
    console.print("  [cyan]1.[/cyan] Desktop Mode - Runs in a native desktop window (pywebview)")
    console.print("  [cyan]2.[/cyan] Web Mode - Opens in your default web browser\n")
    
    while True:
        choice = Prompt.ask(
            "Select mode",
            choices=["1", "2"],
            default="2"
        )
        
        if choice == "1":
            return "desktop"
        else:
            return "web"


def get_app_info():
    """Collect application information"""
    console.print("\n[bold yellow]Step 2: Application Information[/bold yellow]\n")
    
    app_name = Prompt.ask(
        "[cyan]Application Name[/cyan]",
        default="PyReact Fusion"
    )
    
    app_description = Prompt.ask(
        "[cyan]Application Description[/cyan]",
        default="A production-ready full-stack application"
    )
    
    app_version = Prompt.ask(
        "[cyan]Application Version[/cyan]",
        default="1.0.0"
    )
    
    author_name = Prompt.ask(
        "[cyan]Author Name[/cyan]",
        default="Sofiane Khoudour"
    )
    
    author_email = Prompt.ask(
        "[cyan]Author Email[/cyan]",
        default="khoudoursofiane75@gmail.com"
    )
    
    author_github = Prompt.ask(
        "[cyan]Author GitHub[/cyan]",
        default="https://github.com/skmercur"
    )
    
    return {
        "name": app_name,
        "description": app_description,
        "version": app_version,
        "author": {
            "name": author_name,
            "email": author_email,
            "github": author_github
        }
    }


def get_database_config():
    """Get database configuration"""
    console.print("\n[bold yellow]Step 3: Database Configuration[/bold yellow]\n")
    console.print("Which database would you like to use?")
    console.print("  [cyan]1.[/cyan] SQLite (Default - No setup required)")
    console.print("  [cyan]2.[/cyan] PostgreSQL")
    console.print("  [cyan]3.[/cyan] MySQL")
    console.print("  [cyan]4.[/cyan] MongoDB\n")
    
    db_choice = Prompt.ask(
        "Select database",
        choices=["1", "2", "3", "4"],
        default="1"
    )
    
    db_map = {
        "1": "sqlite",
        "2": "postgresql",
        "3": "mysql",
        "4": "mongodb"
    }
    
    return db_map[db_choice]


def get_server_config():
    """Get server configuration"""
    console.print("\n[bold yellow]Step 4: Server Configuration[/bold yellow]\n")
    
    host = Prompt.ask(
        "[cyan]Server Host[/cyan]",
        default="0.0.0.0"
    )
    
    port = Prompt.ask(
        "[cyan]Server Port[/cyan]",
        default="8000"
    )
    
    return {
        "host": host,
        "port": int(port)
    }


def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        console.print(f"\n[green]✓ Configuration saved to {CONFIG_FILE}[/green]")
        return True
    except Exception as e:
        console.print(f"\n[red]✗ Error saving configuration: {e}[/red]")
        return False


def main():
    """Main setup function"""
    print_header()
    
    # Check if config already exists
    if CONFIG_FILE.exists():
        console.print("[yellow]Configuration file already exists.[/yellow]")
        console.print(f"[dim]Current config: {CONFIG_FILE}[/dim]\n")
        
        # Show current config
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                current_config = json.load(f)
                app_info = current_config.get("app", {})
                mode = current_config.get("mode", "web")
                console.print(f"  Mode: {mode.title()}")
                console.print(f"  App Name: {app_info.get('name', 'N/A')}")
                console.print(f"  Version: {app_info.get('version', 'N/A')}\n")
        except:
            pass
        
        overwrite = Confirm.ask(
            "[yellow]Do you want to reconfigure?[/yellow]",
            default=False
        )
        if not overwrite:
            console.print("[green]Using existing configuration.[/green]")
            console.print("[dim]To reconfigure later, run: python scripts/setup.py[/dim]\n")
            return
    
    # Collect information
    mode = get_app_mode()
    app_info = get_app_info()
    database = get_database_config()
    server = get_server_config()
    
    # Build configuration
    config = {
        "mode": mode,
        "app": app_info,
        "database": {
            "type": database
        },
        "server": server
    }
    
    # Save configuration
    if save_config(config):
        console.print("\n[bold green]Setup Complete![/bold green]\n")
        console.print(Panel(
            f"[bold]Mode:[/bold] {mode.title()}\n"
            f"[bold]App Name:[/bold] {app_info['name']}\n"
            f"[bold]Database:[/bold] {database.title()}\n"
            f"[bold]Server:[/bold] {server['host']}:{server['port']}",
            title="Configuration Summary",
            border_style="green",
            box=box.ROUNDED
        ))
        console.print("\n[yellow]Configuration saved![/yellow]")
        console.print("[dim]This configuration will be used automatically on next run.[/dim]\n")
        
        run_now = Confirm.ask(
            "[cyan]Would you like to run the application now?[/cyan]",
            default=True
        )
        
        if run_now:
            console.print("\n[green]Starting application...[/green]\n")
            # Import run script using subprocess to avoid import issues
            import subprocess
            import sys
            subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "run.py")])
        else:
            console.print("\n[yellow]You can run your application later with:[/yellow]")
            console.print("[cyan]  python scripts/run.py[/cyan]\n")
    else:
        console.print("\n[red]Setup failed. Please try again.[/red]\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup cancelled by user.[/yellow]")
        sys.exit(0)

