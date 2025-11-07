"""
Database Models
SQLAlchemy models for SQL databases
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Create Base for SQLAlchemy models
# This will be used only for SQL databases (not MongoDB)
Base = declarative_base()


class User(Base):
    """
    User model for SQL databases
    For MongoDB, use a similar structure but with PyMongo documents
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# MongoDB User Document Structure (for reference)
# {
#     "_id": ObjectId,
#     "email": str,
#     "username": str,
#     "hashed_password": str,
#     "full_name": str,
#     "is_active": bool,
#     "is_superuser": bool,
#     "created_at": datetime,
#     "updated_at": datetime
# }

