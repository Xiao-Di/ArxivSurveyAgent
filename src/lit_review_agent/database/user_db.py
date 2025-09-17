"""User database models and operations for PaperSurveyAgent."""

import os
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from pydantic import BaseModel, validator, EmailStr
from contextlib import contextmanager

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/users.db")

# 确保数据目录存在
data_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
if data_dir and not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base class for models
Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    disabled = Column(Boolean, default=False)

    # 付费系统相关字段
    balance = Column(Float, default=0.0)  # 账户余额
    total_papers_searched = Column(Integer, default=0)  # 累计检索文章数
    total_amount_spent = Column(Float, default=0.0)  # 累计消费金额


# Pydantic models for API
class UserBase(BaseModel):
    """Base user model."""

    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation model."""

    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @validator("username")
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if not v.replace("_", "").isalnum():
            raise ValueError(
                "Username must contain only alphanumeric characters and underscores"
            )
        return v

    @validator("email")
    def validate_email(cls, v):
        # EmailStr 会处理基本的格式验证，我们只需要标准化为小写
        if not v:
            raise ValueError("Email is required")
        return v.lower()  # 标准化为小写


class UserResponse(UserBase):
    """User response model."""

    id: int
    created_at: datetime
    disabled: bool = False

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login model."""

    username: str
    password: str


# 消费记录表
class UsageRecord(Base):
    """SQLAlchemy Usage Record model."""

    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    query = Column(String(500))  # 搜索查询
    papers_count = Column(Integer)  # 检索文章数
    amount_charged = Column(Float)  # 扣费金额
    timestamp = Column(DateTime, default=datetime.utcnow)


# 充值记录表
class RechargeRecord(Base):
    """SQLAlchemy Recharge Record model."""

    __tablename__ = "recharge_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    amount = Column(Float)  # 充值金额
    payment_method = Column(String(50))  # 支付方式
    transaction_id = Column(String(100))  # 交易ID
    status = Column(String(20))  # 状态：pending/success/failed
    timestamp = Column(DateTime, default=datetime.utcnow)


# Pydantic models for API responses
class UsageRecordResponse(BaseModel):
    """Usage record response model."""

    id: int
    query: str
    papers_count: int
    amount_charged: float
    timestamp: datetime

    class Config:
        from_attributes = True


class RechargeRecordResponse(BaseModel):
    """Recharge record response model."""

    id: int
    amount: float
    payment_method: str
    transaction_id: str
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True


class UserBalanceResponse(BaseModel):
    """User balance response model."""

    balance: float
    total_papers_searched: int
    total_amount_spent: float


# Database operations
class UserDatabase:
    """User database operations class."""

    def __init__(self):
        """Initialize database."""
        self.create_tables()

    def create_tables(self):
        """Create database tables."""
        Base.metadata.create_all(bind=engine)

    @contextmanager
    def get_db(self):
        """Get database session context manager."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_user(self, user_data: UserCreate) -> Optional[UserModel]:
        """Create a new user."""
        try:
            with self.get_db() as db:
                # Check if user already exists
                if self.get_user_by_username(db, user_data.username):
                    raise ValueError("Username already exists")

                if self.get_user_by_email(db, user_data.email):
                    raise ValueError("Email already exists")

                # Create new user
                hashed_password = pwd_context.hash(user_data.password)
                db_user = UserModel(
                    username=user_data.username,
                    email=user_data.email,
                    full_name=user_data.full_name,
                    hashed_password=hashed_password,
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return db_user
        except IntegrityError as e:
            raise ValueError("User already exists") from e

    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """Get user by ID."""
        with self.get_db() as db:
            return db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[UserModel]:
        """Get user by username."""
        return db.query(UserModel).filter(UserModel.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[UserModel]:
        """Get user by email."""
        return db.query(UserModel).filter(UserModel.email == email).first()

    def authenticate_user(self, username: str, password: str) -> Optional[UserModel]:
        """Authenticate user credentials."""
        with self.get_db() as db:
            user = self.get_user_by_username(db, username)
            if not user:
                return None
            if not pwd_context.verify(password, user.hashed_password):
                return None
            return user

    def username_exists(self, username: str) -> bool:
        """Check if username exists."""
        with self.get_db() as db:
            return (
                db.query(UserModel).filter(UserModel.username == username).first()
                is not None
            )

    def email_exists(self, email: str) -> bool:
        """Check if email exists."""
        with self.get_db() as db:
            return (
                db.query(UserModel).filter(UserModel.email == email).first() is not None
            )

    def get_all_users(self) -> List[UserModel]:
        """Get all users (admin function)."""
        with self.get_db() as db:
            return db.query(UserModel).all()

    def update_user(self, user_id: int, **kwargs) -> Optional[UserModel]:
        """Update user information."""
        with self.get_db() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return None

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            user.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)
            return user

    def disable_user(self, user_id: int) -> Optional[UserModel]:
        """Disable a user account."""
        return self.update_user(user_id, disabled=True)

    def enable_user(self, user_id: int) -> Optional[UserModel]:
        """Enable a user account."""
        return self.update_user(user_id, disabled=False)

    def delete_user(self, user_id: int) -> bool:
        """Delete a user account."""
        with self.get_db() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return False

            db.delete(user)
            db.commit()
            return True

    # 余额管理相关方法
    def get_user_balance(self, user_id: int) -> Optional[UserBalanceResponse]:
        """获取用户余额信息."""
        with self.get_db() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return None

            return UserBalanceResponse(
                balance=user.balance,
                total_papers_searched=user.total_papers_searched,
                total_amount_spent=user.total_amount_spent,
            )

    def add_balance(
        self,
        user_id: int,
        amount: float,
        payment_method: str = "alipay",
        transaction_id: str = None,
    ) -> bool:
        """用户充值."""
        if amount <= 0:
            return False

        with self.get_db() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                return False

            # 更新用户余额
            user.balance += amount
            user.updated_at = datetime.now(timezone.utc)

            # 创建充值记录
            recharge_record = RechargeRecord(
                user_id=user_id,
                amount=amount,
                payment_method=payment_method,
                transaction_id=transaction_id
                or f"manual_{int(datetime.utcnow().timestamp())}",
                status="success",
            )
            db.add(recharge_record)

            db.commit()
            return True

    def deduct_balance(
        self, user_id: int, amount: float, papers_count: int, query: str
    ) -> bool:
        """扣除用户余额."""
        if amount <= 0:
            return False

        with self.get_db() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user or user.balance < amount:
                return False

            # 扣除余额
            user.balance -= amount
            user.total_papers_searched += papers_count
            user.total_amount_spent += amount
            user.updated_at = datetime.now(timezone.utc)

            # 创建消费记录
            usage_record = UsageRecord(
                user_id=user_id,
                query=query,
                papers_count=papers_count,
                amount_charged=amount,
            )
            db.add(usage_record)

            db.commit()
            return True

    def check_balance_sufficient(self, user_id: int, required_amount: float) -> bool:
        """检查余额是否足够."""
        with self.get_db() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            return user and user.balance >= required_amount

    def get_usage_history(
        self, user_id: int, limit: int = 50
    ) -> List[UsageRecordResponse]:
        """获取用户使用历史."""
        with self.get_db() as db:
            records = (
                db.query(UsageRecord)
                .filter(UsageRecord.user_id == user_id)
                .order_by(UsageRecord.timestamp.desc())
                .limit(limit)
                .all()
            )

            return [
                UsageRecordResponse(
                    id=record.id,
                    query=record.query,
                    papers_count=record.papers_count,
                    amount_charged=record.amount_charged,
                    timestamp=record.timestamp,
                )
                for record in records
            ]

    def get_recharge_history(
        self, user_id: int, limit: int = 50
    ) -> List[RechargeRecordResponse]:
        """获取用户充值历史."""
        with self.get_db() as db:
            records = (
                db.query(RechargeRecord)
                .filter(RechargeRecord.user_id == user_id)
                .order_by(RechargeRecord.timestamp.desc())
                .limit(limit)
                .all()
            )

            return [
                RechargeRecordResponse(
                    id=record.id,
                    amount=record.amount,
                    payment_method=record.payment_method,
                    transaction_id=record.transaction_id,
                    status=record.status,
                    timestamp=record.timestamp,
                )
                for record in records
            ]

    def calculate_search_cost(self, papers_count: int) -> float:
        """计算搜索费用."""
        # 单价：0.1元/篇，最低消费0.5元
        cost = papers_count * 0.1
        return max(cost, 0.5)  # 最低消费0.5元


# Global user database instance
user_db = UserDatabase()


# Create default user if it doesn't exist
def create_default_user(max_retries=3):
    """Create default user for testing purposes with retry mechanism."""
    import time

    for attempt in range(max_retries):
        try:
            # Ensure database tables exist
            user_db.create_tables()

            default_user = UserCreate(
                username="xiaodi",
                email="xiaodi@example.com",
                password="xiaodi_shishen",
                full_name="Default User",
            )

            # Check if user already exists first
            if user_db.username_exists(default_user.username):
                # print("ℹ️ Default user 'xiaodi' already exists")
                return True

            user_db.create_user(default_user)
            # print("✅ Default user 'xiaodi' created successfully")
            return True

        except ValueError as e:
            if "already exists" in str(e):
                # print("ℹ️ Default user 'xiaodi' already exists")
                return True
            else:
                print(f"⚠️ Validation error creating default user: {e}")

        except Exception as e:
            print(
                f"⚠️ Error creating default user (attempt {attempt + 1}/{max_retries}): {e}"
            )
            if attempt < max_retries - 1:
                print("🔄 Retrying in 2 seconds...")
                time.sleep(2)

    print(f"❌ Failed to create default user after {max_retries} attempts")
    return False


# Initialize default user with retry mechanism
def initialize_user_system():
    """Initialize the complete user system with proper error handling."""
    # print("🔧 Initializing user authentication system...")

    try:
        # First ensure database tables are created
        user_db.create_tables()
        # print("✅ Database tables created/verified")

        # Then create default user
        if create_default_user():
            # print("✅ User authentication system initialized successfully")
            return True
        else:
            print("⚠️ User authentication system initialized with warnings")
            return False

    except Exception as e:
        print(f"❌ Critical error initializing user system: {e}")
        return False


# Initialize user system on module import
initialize_user_system()
