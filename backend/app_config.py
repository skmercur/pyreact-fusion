"""
Application Configuration Loader
Loads configuration from app_config.json
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "app_config.json"


def load_app_config() -> Optional[Dict[str, Any]]:
    """Load application configuration from JSON file"""
    if not CONFIG_FILE.exists():
        return None
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def get_app_info() -> Dict[str, Any]:
    """Get application information from config"""
    config = load_app_config()
    
    if config and "app" in config:
        return config["app"]
    
    # Default values
    return {
        "name": "PyReact Fusion",
        "description": "A production-ready full-stack application template",
        "version": "1.0.0",
        "author": {
            "name": "Sofiane Khoudour",
            "email": "khoudoursofiane75@gmail.com",
            "github": "https://github.com/skmercur"
        }
    }


def get_app_mode() -> str:
    """Get application mode (desktop or web)"""
    config = load_app_config()
    if config and "mode" in config:
        return config.get("mode", "web")
    return "web"

