"""
Database Connection Factory
Supports multiple database types: SQLite, PostgreSQL, MySQL, MongoDB
"""
from enum import Enum
from typing import Optional, Union
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
import os

from backend.config import settings


class DatabaseType(str, Enum):
    """Supported database types"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"


class DatabaseFactory:
    """Factory class for creating database connections"""
    
    @staticmethod
    def create_sqlite_engine(db_path: str) -> Engine:
        """Create SQLite database engine"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
        return create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            echo=settings.debug
        )
    
    @staticmethod
    def create_postgresql_engine(
        host: str,
        port: int,
        database: str,
        user: str,
        password: str
    ) -> Engine:
        """Create PostgreSQL database engine"""
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return create_engine(
            connection_string,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=settings.debug
        )
    
    @staticmethod
    def create_mysql_engine(
        host: str,
        port: int,
        database: str,
        user: str,
        password: str
    ) -> Engine:
        """Create MySQL database engine"""
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        return create_engine(
            connection_string,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=settings.debug
        )
    
    @staticmethod
    def create_mongodb_client(
        host: str,
        port: int,
        database: str,
        user: Optional[str] = None,
        password: Optional[str] = None
    ) -> MongoDatabase:
        """Create MongoDB client and return database"""
        if user and password:
            connection_string = f"mongodb://{user}:{password}@{host}:{port}/{database}"
        else:
            connection_string = f"mongodb://{host}:{port}/{database}"
        
        client = MongoClient(connection_string)
        return client[database]
    
    @staticmethod
    def create_engine() -> Union[Engine, MongoDatabase]:
        """Create database engine based on configuration"""
        db_type = settings.database_type.lower()
        
        if db_type == DatabaseType.SQLITE:
            return DatabaseFactory.create_sqlite_engine(settings.sqlite_db_path)
        
        elif db_type == DatabaseType.POSTGRESQL:
            return DatabaseFactory.create_postgresql_engine(
                settings.postgres_host,
                settings.postgres_port,
                settings.postgres_db,
                settings.postgres_user,
                settings.postgres_password
            )
        
        elif db_type == DatabaseType.MYSQL:
            return DatabaseFactory.create_mysql_engine(
                settings.mysql_host,
                settings.mysql_port,
                settings.mysql_db,
                settings.mysql_user,
                settings.mysql_password
            )
        
        elif db_type == DatabaseType.MONGODB:
            return DatabaseFactory.create_mongodb_client(
                settings.mongodb_host,
                settings.mongodb_port,
                settings.mongodb_db,
                settings.mongodb_user if settings.mongodb_user else None,
                settings.mongodb_password if settings.mongodb_password else None
            )
        
        else:
            raise ValueError(f"Unsupported database type: {db_type}")


# Create database engine
db_engine = DatabaseFactory.create_engine()

# For SQL databases, create session factory
if isinstance(db_engine, Engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
else:
    # MongoDB doesn't use SQLAlchemy sessions
    SessionLocal = None

# Import Base from models (only available for SQL databases)
try:
    from backend.database.models import Base
except ImportError:
    Base = None


def get_database() -> Union[Session, MongoDatabase]:
    """
    Get database session/client
    Returns SQLAlchemy session for SQL databases or MongoDB database for MongoDB
    """
    if isinstance(db_engine, Engine):
        # SQL database - return session
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        # MongoDB - return database directly
        yield db_engine

