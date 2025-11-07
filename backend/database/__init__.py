"""
Database Package
Provides database connection and models
"""

from .connection import get_database, DatabaseFactory, DatabaseType, db_engine

# Import models only if Base is available (SQL databases)
try:
    from .models import Base, User
    __all__ = ["get_database", "DatabaseFactory", "DatabaseType", "Base", "User", "db_engine"]
except (ImportError, AttributeError):
    # MongoDB doesn't use SQLAlchemy models
    Base = None
    User = None
    __all__ = ["get_database", "DatabaseFactory", "DatabaseType", "db_engine"]

