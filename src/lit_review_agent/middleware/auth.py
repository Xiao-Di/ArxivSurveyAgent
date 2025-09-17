"""JWT Authentication middleware for the literature review agent."""

import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Import user database with enhanced error handling
try:
    from src.lit_review_agent.database.user_db import user_db, UserModel
    USER_DB_AVAILABLE = True
    print("✅ Authentication module: User database imported successfully")
except ImportError as e:
    user_db = None
    UserModel = None
    USER_DB_AVAILABLE = False
    print(f"⚠️ Authentication module: Failed to import user database - {e}")


# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


class Token(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model."""

    username: Optional[str] = None


class User(BaseModel):
    """User model."""
    id: Optional[int] = None
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    created_at: Optional[datetime] = None


class UserInDB(User):
    """User in database model."""
    hashed_password: str


# Legacy users_db for backward compatibility
users_db = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def get_user(db: Dict[str, Any], username: str) -> Optional[UserInDB]:
    """Get user from database (legacy function)."""
    if user_db is None:
        return None

    # Try to get user from new database
    with user_db.get_db() as session:
        user = user_db.get_user_by_username(session, username)
        if user:
            return UserInDB(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                hashed_password=user.hashed_password,
                disabled=user.disabled,
                created_at=user.created_at
            )

    # Fallback to legacy in-memory database
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(
    db: Dict[str, Any], username: str, password: str
) -> Optional[UserInDB]:
    """Authenticate user credentials."""
    if user_db is None:
        return None

    # Use new database authentication
    user_model = user_db.authenticate_user(username, password)
    if user_model:
        return UserInDB(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            full_name=user_model.full_name,
            hashed_password=user_model.hashed_password,
            disabled=user_model.disabled,
            created_at=user_model.created_at
        )

    return None


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """Verify JWT token and return payload."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise credentials_exception

    return payload


async def get_current_user(
    token_payload: Dict[str, Any] = Depends(verify_token),
) -> User:
    """Get current user from token."""
    username = token_payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = get_user(users_db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user."""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def create_user(username: str, email: str, password: str, full_name: Optional[str] = None) -> Optional[UserInDB]:
    """Create a new user."""
    if not USER_DB_AVAILABLE or user_db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User authentication service is currently unavailable"
        )

    try:
        from src.lit_review_agent.database.user_db import UserCreate
        user_data = UserCreate(
            username=username,
            email=email,
            password=password,
            full_name=full_name
        )
        user_model = user_db.create_user(user_data)
        if user_model:
            return UserInDB(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                full_name=user_model.full_name,
                hashed_password=user_model.hashed_password,
                disabled=user_model.disabled,
                created_at=user_model.created_at
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        print(f"❌ Error creating user '{username}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user due to server error"
        ) from e

    return None


def check_username_exists(username: str) -> bool:
    """Check if username already exists."""
    if not USER_DB_AVAILABLE or user_db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User authentication service is currently unavailable"
        )
    return user_db.username_exists(username)


def check_email_exists(email: str) -> bool:
    """Check if email already exists."""
    if not USER_DB_AVAILABLE or user_db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User authentication service is currently unavailable"
        )
    return user_db.email_exists(email)


class AuthMiddleware:
    """Authentication middleware class."""

    def __init__(self):
        self.security = HTTPBearer()

    async def __call__(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        """Middleware call method."""
        return await verify_token(credentials)
