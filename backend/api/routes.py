"""
API Routes
Main API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pymongo.database import Database
from typing import Union
from pydantic import BaseModel, EmailStr

from backend.database import get_database, db_engine
from backend.database.connection import DatabaseType
from backend.database.models import User, Base
from backend.services.auth import AuthService
from backend.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")


# Pydantic models for request/response
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str = None
    is_active: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class HealthResponse(BaseModel):
    status: str
    environment: str
    database: str
    app_name: str = None
    app_version: str = None
    mode: str = None


# Dependency to get current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Union[Session, Database] = Depends(get_database)
) -> dict:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = AuthService.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # Get user from database
    from pymongo.database import Database as MongoDatabase
    
    if isinstance(db, Session) and User is not None:
        # SQL database
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
    elif isinstance(db, MongoDatabase):
        # MongoDB
        user = db.users.find_one({"username": username})
        if user is None:
            raise credentials_exception
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "is_active": user.get("is_active", True)
        }
    else:
        raise credentials_exception


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from backend.app_config import get_app_info, get_app_mode
    
    try:
        # Test database connection
        from pymongo.database import Database as MongoDatabase
        
        if isinstance(db_engine, MongoDatabase):
            # MongoDB
            db_engine.command("ping")
            db_status = "connected"
        else:
            # SQL database
            from sqlalchemy import text
            with db_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    app_info = get_app_info()
    app_mode = get_app_mode()
    
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        database=db_status,
        app_name=app_info.get("name"),
        app_version=app_info.get("version"),
        mode=app_mode
    )


@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Union[Session, Database] = Depends(get_database)
):
    """Register a new user"""
    auth_service = AuthService()
    
    # Check if user exists
    from pymongo.database import Database as MongoDatabase
    
    if isinstance(db, Session) and User is not None:
        # SQL database
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        # Create new user
        hashed_password = auth_service.get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            full_name=new_user.full_name,
            is_active=new_user.is_active
        )
    elif isinstance(db, MongoDatabase):
        # MongoDB
        existing_user = db.users.find_one({
            "$or": [
                {"email": user_data.email},
                {"username": user_data.username}
            ]
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        # Create new user
        from datetime import datetime
        hashed_password = auth_service.get_password_hash(user_data.password)
        user_doc = {
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": hashed_password,
            "full_name": user_data.full_name,
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = db.users.insert_one(user_doc)
        
        return UserResponse(
            id=str(result.inserted_id),
            email=user_doc["email"],
            username=user_doc["username"],
            full_name=user_doc["full_name"],
            is_active=user_doc["is_active"]
        )


@router.post("/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Union[Session, Database] = Depends(get_database)
):
    """Login and get access token"""
    auth_service = AuthService()
    
    # Get user from database
    from pymongo.database import Database as MongoDatabase
    
    if isinstance(db, Session) and User is not None:
        # SQL database
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
    elif isinstance(db, MongoDatabase):
        # MongoDB
        user = db.users.find_one({"username": form_data.username})
        if not user or not auth_service.verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database configuration error"
        )
    
    # Create access token
    access_token = auth_service.create_access_token(data={"sub": form_data.username})
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/auth/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Union[Session, Database] = Depends(get_database)
):
    """Get list of users (requires authentication)"""
    from pymongo.database import Database as MongoDatabase
    
    if isinstance(db, Session) and User is not None:
        # SQL database
        users = db.query(User).offset(skip).limit(limit).all()
        return [
            UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active
            )
            for user in users
        ]
    elif isinstance(db, MongoDatabase):
        # MongoDB
        users = list(db.users.find().skip(skip).limit(limit))
        return [
            UserResponse(
                id=str(user["_id"]),
                email=user["email"],
                username=user["username"],
                full_name=user.get("full_name"),
                is_active=user.get("is_active", True)
            )
            for user in users
        ]
    else:
        return []

