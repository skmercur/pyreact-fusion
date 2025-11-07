"""
PyReact Fusion - Main Application Entry Point
FastAPI application with static file serving and API routes
"""
import logging
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.config import settings
from backend.app_config import get_app_info, get_app_mode
from backend.api.routes import router
from backend.api.middleware import setup_middleware
from backend.database.connection import db_engine, DatabaseType
from backend.database.models import Base

# Configure logging
os.makedirs(os.path.dirname(settings.log_file) if os.path.dirname(settings.log_file) else ".", exist_ok=True)
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Get app info from config
app_info = get_app_info()
app_mode = get_app_mode()

# Create FastAPI app
app = FastAPI(
    title=app_info.get("name", settings.app_name),
    version=app_info.get("version", settings.app_version),
    description=app_info.get("description", "Production-ready full-stack application template"),
    docs_url="/api/docs" if settings.is_development else None,
    redoc_url="/api/redoc" if settings.is_development else None,
)

# Setup middleware
setup_middleware(app)

# Include API routes
app.include_router(router, prefix=settings.api_prefix)


# Initialize database tables (for SQL databases only)
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    app_name = app_info.get("name", settings.app_name)
    app_version = app_info.get("version", settings.app_version)
    logger.info(f"Starting {app_name} v{app_version}")
    logger.info(f"Mode: {app_mode.title()}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database type: {settings.database_type}")
    
    # Create tables for SQL databases
    from sqlalchemy import Engine
    
    if settings.database_type.lower() != DatabaseType.MONGODB and Base is not None and isinstance(db_engine, Engine):
        try:
            Base.metadata.create_all(bind=db_engine)
            logger.info("Database tables initialized")
        except Exception as e:
            logger.error(f"Error initializing database tables: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application")


# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()}
    )


# Serve static files (React app)
frontend_path = Path(settings.frontend_build_path).resolve()

if frontend_path.exists() and (frontend_path / "index.html").exists():
    # Mount static files directory - this must come BEFORE the catch-all route
    static_dir = frontend_path / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        logger.info(f"Mounted static files from: {static_dir}")
    
    # Serve index.html for root
    @app.get("/")
    async def serve_root():
        """Serve React app index.html for root path"""
        index_file = frontend_path / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return JSONResponse(status_code=404, content={"error": "Index file not found"})
    
    # Serve index.html for all other non-API routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str, request: Request):
        """Serve React app for all non-API routes"""
        # Don't serve SPA for API routes or static files
        if (full_path.startswith("api/") or 
            full_path.startswith("docs") or 
            full_path.startswith("redoc") or 
            full_path.startswith("openapi.json") or
            full_path.startswith("static/")):
            return JSONResponse(status_code=404, content={"error": "Not found"})
        
        # Serve index.html for all other routes (SPA fallback)
        index_file = frontend_path / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        else:
            return JSONResponse(
                status_code=404,
                content={"error": "Frontend not built. Run 'python scripts/build_frontend.py' first."}
            )
    
    logger.info(f"Frontend will be served from: {frontend_path}")
else:
    logger.warning(f"Frontend build path not found: {frontend_path}")
    logger.warning("Run 'python scripts/build_frontend.py' to build the frontend")
    
    # Still serve a basic response for root
    @app.get("/")
    async def root():
        return JSONResponse(
            status_code=503,
            content={
                "error": "Frontend not built",
                "message": "Please run 'python scripts/build_frontend.py' to build the frontend"
            }
        )


def main():
    """Main entry point for running the application"""
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development and settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()

