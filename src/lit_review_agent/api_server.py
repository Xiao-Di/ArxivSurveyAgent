#!/usr/bin/env python3
"""
FastAPI 服务器 - 为 Vue3 前端提供 API 接口
"""

import asyncio
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta

# 添加src目录到Python路径
current_dir = Path(__file__).parent.parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from src.lit_review_agent.agent import LiteratureAgent
    from src.lit_review_agent.utils.config import Config
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    LiteratureAgent = None
    Config = None

# 导入认证中间件 - 移除过度宽泛的异常处理
# print("🔧 Importing authentication middleware...")
try:
    from src.lit_review_agent.middleware.auth import (
        authenticate_user,
        create_access_token,
        create_user,
        check_username_exists,
        check_email_exists,
        users_db,
        ACCESS_TOKEN_EXPIRE_MINUTES,
        Token,
        User as AuthUser,
        get_current_active_user,
    )

    # print("✅ Authentication middleware imported successfully")
except ImportError as e:
    print(f"❌ Critical error importing authentication middleware: {e}")
    raise

# 导入用户数据库
# print("🔧 Importing user database...")
try:
    from src.lit_review_agent.database.user_db import user_db

    # print("✅ User database imported successfully")
except ImportError as e:
    print(f"❌ Critical error importing user database: {e}")
    raise

# 暂时禁用限流器
limiter = None

# 认证中间件已成功导入，无需临时模型


# 临时装饰器定义，直到实现真正的速率限制


def rate_limit_auth(func):
    """临时认证速率限制装饰器"""
    return func


def rate_limit_search(func):
    """临时搜索速率限制装饰器"""
    return func


def rate_limit_api(func):
    """临时API速率限制装饰器"""
    return func


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    print(">> 启动 AI Literature Review API 服务器...")
    try:
        agent = get_agent()
        if agent:
            print(">> 文献代理初始化成功")
        else:
            print(">> 文献代理初始化失败，将使用模拟数据")
    except Exception as e:
        print(f">> 代理初始化异常: {e}")
        print(">> 将使用模拟数据模式运行")

    yield

    # 关闭时清理
    print(">> 关闭 AI Literature Review API 服务器...")
    global literature_agent
    if literature_agent:
        try:
            # 清理资源
            literature_agent = None
            print(">> 资源清理完成")
        except Exception as e:
            print(f">> 资源清理异常: {e}")


# 创建 FastAPI 应用
app = FastAPI(
    title="AI Literature Review API",
    description="智能文献综述系统 API",
    version="1.1",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "file://",
        "*",  # 开发环境允许所有源
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件服务 - 用于收款码图片
from fastapi.staticfiles import StaticFiles

try:
    app.mount("/media", StaticFiles(directory="./media"), name="media")
    print("✅ Static files service configured for /media")
except Exception as e:
    print(f"⚠️ Failed to configure static files service: {e}")

# 添加安全中间件
if limiter:
    app.state.limiter = limiter

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

# 如果用户认证函数不可用，抛出错误而不是使用临时用户
if get_current_active_user is None:

    async def get_current_active_user():
        """认证服务不可用时抛出错误"""
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User authentication service is currently unavailable. Please try again later.",
        )


# 请求模型
class SearchRequest(BaseModel):
    query: Optional[str] = None  # Legacy structured query field
    rawQuery: Optional[str] = None  # New natural language query field
    sources: List[str] = ["arxiv"]  # Only ArXiv supported
    maxPapers: int = 5
    yearStart: Optional[int] = None
    yearEnd: Optional[int] = None
    retrieveFullText: bool = False
    enableAIAnalysis: bool = True


class QuickSearchRequest(BaseModel):
    query: str = "machine learning"
    maxPapers: int = 3


class ReportRequest(BaseModel):
    papers: List[Dict]
    title: str


# 响应模型
class Paper(BaseModel):
    title: str
    authors: List[str]
    publishedDate: str
    source: str
    summary: str
    keywords: Optional[List[str]] = []
    url: Optional[str] = None
    pdfUrl: Optional[str] = None
    fullTextRetrieved: Optional[bool] = False


class SearchResult(BaseModel):
    papers: List[Paper]
    totalCount: int
    processingTime: float
    summary: Optional[str] = None
    actionPlan: Optional[List[str]] = None


# 全局变量
literature_agent = None


def get_agent():
    """获取文献代理实例"""
    global literature_agent
    if literature_agent is None:
        try:
            print(">> 正在初始化完整文献代理...")
            # 尝试初始化完整代理
            literature_agent = LiteratureAgent()
            print(">> 完整文献代理初始化成功")
            return literature_agent
        except Exception as e:
            print(f">> 完整代理初始化失败，使用简化版: {e}")
            # 如果完整代理初始化失败，回退到简化版
            from src.lit_review_agent.retrieval.arxiv_client import ArxivClient

            # Semantic Scholar removed - using ArXiv only

            # 创建简化的代理对象
            class SimpleLiteratureAgent:
                def __init__(self):
                    print(">> 初始化简化代理...")
                    self.arxiv_client = ArxivClient(max_results=100)
                    print(">> 简化代理初始化完成")

                async def conduct_literature_review(self, **kwargs):
                    """快速搜索方法 - 专注速度"""
                    query = (
                        kwargs.get("raw_query")
                        or kwargs.get("research_topic")
                        or kwargs.get("query")
                    )
                    max_papers = kwargs.get("max_papers", 5)
                    sources = kwargs.get("sources", ["arxiv"])

                    print(f">> 快速搜索: {query}")

                    all_papers = []

                    # 仅使用ArXiv
                    if "arxiv" in sources:
                        try:
                            print(">> 快速搜索ArXiv...")
                            arxiv_results = await asyncio.wait_for(
                                self.arxiv_client.search(
                                    query=query,
                                    max_results=min(max_papers, 5),  # 最多5篇
                                ),
                                timeout=30,  # 30秒超时
                            )
                            all_papers.extend(arxiv_results)
                            print(f">> 获取到 {len(arxiv_results)} 篇论文")
                        except Exception as e:
                            print(f">> 搜索失败: {e}")
                            # 返回空结果而不是抛出异常
                            all_papers = []

                    print(f">> 完成，共 {len(all_papers)} 篇论文")

                    # 如果没有找到任何论文，返回说明而不是抛出异常
                    if len(all_papers) == 0:
                        print(">> 未找到论文，返回空结果")
                        return {
                            "processed_papers": [],
                            "action_plan": [
                                f"🔍 搜索查询：{query}",
                                "⚠️ 未找到匹配的论文",
                                "💡 建议：尝试不同的关键词或扩大搜索范围",
                                "🌐 数据源：Semantic Scholar",
                            ],
                        }

                    # 转换为API格式
                    processed_papers = []
                    for paper in all_papers:
                        processed_papers.append(
                            {
                                "title": paper.title,
                                "authors": paper.authors,
                                "published_date": (
                                    paper.publication_date.isoformat()
                                    if paper.publication_date
                                    else ""
                                ),
                                "source": paper.source,
                                "summary": paper.abstract or "",
                                "keywords": [],
                                "url": paper.url,
                                "pdf_url": paper.pdf_url or "",
                                "full_text_retrieved": False,
                            }
                        )

                    return {
                        "processed_papers": processed_papers,
                        "action_plan": [
                            f"🎯 确定研究主题：{query}",
                            "📚 选择数据源：arXiv",
                            f"🔎 执行检索策略：检索最多{max_papers}篇相关论文",
                            "📊 分析论文元数据：标题、作者、摘要等",
                            "📝 整理搜索结果",
                        ],
                    }

            literature_agent = SimpleLiteratureAgent()
            print(">> 简化文献代理初始化成功")
        except Exception as e:
            print(f">> 代理初始化失败: {e}")
            print(">> 将使用模拟数据模式")
            literature_agent = None
    return literature_agent


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI Literature Review Agent API",
        "version": "1.1",
        "status": "running",
    }


# 认证端点
@app.post("/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录获取访问token"""
    # 检查认证服务是否可用
    if user_db is None or create_access_token is None:
        print("❌ Authentication service unavailable during login attempt")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is currently unavailable. Please try again later.",
        )

    # 输入验证
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required",
        )

    # 使用user_db进行认证
    try:
        user = user_db.authenticate_user(form_data.username, form_data.password)
        if not user:
            print(f"❌ Authentication failed for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        print(f"❌ Authentication error for user {form_data.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed due to server error",
        )

    # 创建访问token
    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        print(f"✅ User '{form_data.username}' logged in successfully")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"❌ Token creation error for user {form_data.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token",
        )


@app.get("/auth/me", response_model=AuthUser)
async def read_users_me(current_user: AuthUser = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user


# User registration models
class UserRegistration(BaseModel):
    """User registration model."""

    username: str
    email: str
    password: str
    full_name: Optional[str] = None


class UsernameCheck(BaseModel):
    """Username check model."""

    username: str


class EmailCheck(BaseModel):
    """Email check model."""

    email: str


@app.post("/auth/register")
async def register_user(user_data: UserRegistration):
    """用户注册"""
    # 检查认证服务是否可用
    if user_db is None or create_access_token is None:
        print("❌ Registration service unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User registration service is currently unavailable. Please try again later.",
        )

    # 输入验证
    if not user_data.username or not user_data.email or not user_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username, email, and password are required",
        )

    try:
        # 使用认证模块的功能进行验证
        # Email format validation is now handled by UserCreate model validators
        # Check if username already exists
        if check_username_exists(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        # Check if email already exists (convert to lowercase as per validation)
        email_lower = user_data.email.lower()
        if check_email_exists(email_lower):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        # Create user using auth module function
        user_in_db = create_user(
            username=user_data.username,
            email=email_lower,  # 使用标准化的小写邮箱
            password=user_data.password,
            full_name=user_data.full_name,
        )

        if not user_in_db:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            )

        # Create access token for automatic login
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_in_db.username}, expires_delta=access_token_expires
        )

        print(f"✅ User '{user_data.username}' registered successfully")
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_in_db.id,
                "username": user_in_db.username,
                "email": user_in_db.email,
                "full_name": user_in_db.full_name,
                "created_at": user_in_db.created_at,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Registration error for user '{user_data.username}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to server error",
        ) from e


@app.post("/auth/check-username")
async def check_username(request: UsernameCheck):
    """检查用户名是否可用"""
    # 检查认证服务是否可用
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Username check service is currently unavailable. Please try again later.",
        )

    try:
        username_available = not check_username_exists(request.username)
        return {"username": request.username, "available": username_available}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Username check error for '{request.username}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Username check failed due to server error",
        ) from e


@app.post("/auth/check-email")
async def check_email(request: EmailCheck):
    """检查邮箱是否可用"""
    # 检查认证服务是否可用
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email check service is currently unavailable. Please try again later.",
        )

    try:
        # 标准化邮箱为小写进行检查
        email_lower = request.email.lower()
        email_available = not check_email_exists(email_lower)
        return {"email": request.email, "available": email_available}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Email check error for '{request.email}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email check failed due to server error",
        ) from e


@app.post("/api/quick-search")
async def quick_search(request: QuickSearchRequest):
    """快速搜索端点 - 使用ArXiv"""
    try:
        print(">> 快速搜索端点被调用")

        # 处理查询字符串编码问题
        query = request.query.strip()
        max_papers = request.maxPapers

        print(f">> 接收到查询: {repr(query)}")  # 使用repr显示原始字符串

        # 检测并修复编码问题
        if query and (
            "?" in query
            or len(query.encode("utf-8", errors="ignore")) != len(query.encode("utf-8"))
        ):
            print(f">> 检测到编码问题，尝试修复...")
            # 如果查询包含问号或编码异常，可能是中文查询被损坏
            # 提供一些常见中文查询的映射
            chinese_query_mapping = {
                "????": "deep learning",
                "????????": "machine learning",
                "????????????": "artificial intelligence",
                "??????": "neural network",
                "??????????": "computer vision",
                "????????????": "natural language processing",
            }

            if query in chinese_query_mapping:
                original_query = query
                query = chinese_query_mapping[query]
                print(f">> 映射损坏的查询: '{original_query}' -> '{query}'")
            elif "?" in query:
                # 如果包含问号但不在映射中，使用默认查询
                print(f">> 查询包含损坏字符，使用默认查询")
                query = "machine learning"

        agent = get_agent()
        if agent:
            print(f">> 使用ArXiv搜索: {query}")
            results = await agent.conduct_literature_review(
                raw_query=query,
                max_papers=max_papers,
                sources=["arxiv"],
                retrieve_full_text=False,
            )

            processed_papers = results.get("processed_papers", [])
            papers = []
            for paper in processed_papers:
                papers.append(
                    {
                        "title": paper.get("title", ""),
                        "authors": paper.get("authors", []),
                        "publishedDate": paper.get("published_date", ""),
                        "source": paper.get("source", "arxiv"),
                        "summary": paper.get("summary", ""),
                        "url": paper.get("url", ""),
                    }
                )

            return {
                "papers": papers,
                "totalCount": len(papers),
                "processingTime": 1.0,
                "summary": f"从ArXiv检索到{len(papers)}篇论文",
            }
        else:
            # 如果代理不可用，返回模拟数据
            return {
                "papers": [
                    {
                        "title": "Attention Is All You Need",
                        "authors": ["Ashish Vaswani", "Noam Shazeer"],
                        "publishedDate": "2017-06-12",
                        "source": "test",
                        "summary": "The dominant sequence transduction models...",
                        "url": "https://arxiv.org/abs/1706.03762",
                    }
                ],
                "totalCount": 1,
                "processingTime": 0.1,
                "summary": "代理不可用，返回模拟数据",
            }
    except Exception as e:
        print(f">> 快速搜索失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        agent = get_agent()
        agent_status = "healthy" if agent else "degraded"

        # 检查认证系统状态
        auth_status = "healthy"
        auth_details = {}
        if user_db is not None:
            try:
                # 测试数据库连接
                with user_db.get_db() as db:
                    # 简单的数据库连接测试
                    pass
                auth_status = "healthy"
                auth_details = {
                    "user_database": "connected",
                    "default_user": "available",
                }
            except Exception as auth_error:
                auth_status = "degraded"
                auth_details = {"user_database": "error", "error": str(auth_error)}
        else:
            auth_status = "unavailable"
            auth_details = {"user_database": "not_available"}

        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "agent_status": agent_status,
            "auth_status": auth_status,
            "version": "1.1",
            "services": {
                "api": "running",
                "agent": agent_status,
                "authentication": auth_status,
                "database": "connected" if agent else "unavailable",
            },
            "details": {"authentication": auth_details},
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "agent_status": "error",
            "auth_status": "error",
        }


@app.get("/auth/health")
async def auth_health_check():
    """认证系统专门的健康检查端点"""
    try:
        if user_db is None:
            return {
                "status": "unavailable",
                "message": "User authentication service is not available",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "user_database": "not_available",
                    "token_service": "unknown",
                },
            }

        # 测试数据库连接
        try:
            with user_db.get_db() as db:
                # 测试默认用户是否存在
                default_user = user_db.get_user_by_username(db, "xiaodi")
                default_user_exists = default_user is not None

            return {
                "status": "healthy",
                "message": "User authentication service is operating normally",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "user_database": "connected",
                    "token_service": "available",
                    "default_user": "available" if default_user_exists else "missing",
                },
                "default_user_info": {
                    "exists": default_user_exists,
                    "username": "xiaodi" if default_user_exists else None,
                },
            }
        except Exception as db_error:
            return {
                "status": "degraded",
                "message": "User database connection issues detected",
                "timestamp": datetime.now().isoformat(),
                "error": str(db_error),
                "components": {
                    "user_database": "connection_error",
                    "token_service": "available",
                },
            }

    except Exception as e:
        return {
            "status": "error",
            "message": "Authentication health check failed",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "components": {"user_database": "error", "token_service": "unknown"},
        }


@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    agent = get_agent()
    return {
        "status": "healthy" if agent else "demo",
        "timestamp": datetime.now().isoformat(),
        "agent_initialized": agent is not None,
    }


@app.post("/api/search", response_model=SearchResult)
@rate_limit_search
async def search_literature(
    request: SearchRequest, current_user: AuthUser = Depends(get_current_active_user)
):
    """文献检索"""
    start_time = time.time()

    try:
        agent = get_agent()

        # Determine which query to use
        query_to_use = request.rawQuery or request.query
        if not query_to_use:
            raise HTTPException(
                status_code=400, detail="Either 'query' or 'rawQuery' must be provided"
            )

        print(f"开始检索: {query_to_use}")

        # 余额检查和费用计算
        if user_db:
            # 获取真实用户信息
            with user_db.get_db() as db:
                real_user = user_db.get_user_by_username(db, current_user.username)
                if real_user:
                    # 计算搜索费用
                    search_cost = user_db.calculate_search_cost(request.maxPapers)

                    # 检查余额是否足够
                    if not user_db.check_balance_sufficient(real_user.id, search_cost):
                        raise HTTPException(
                            status_code=402,
                            detail={
                                "error": "Insufficient balance",
                                "required": search_cost,
                                "current_balance": (
                                    user_db.get_user_balance(real_user.id).balance
                                    if user_db.get_user_balance(real_user.id)
                                    else 0
                                ),
                                "message": f"余额不足，需要{search_cost:.2f}元，请充值后再试",
                            },
                        )

                    print(f">> 余额检查通过，将扣除{search_cost:.2f}元")
                else:
                    # 用户不存在，跳过费用检查
                    search_cost = 0
                    print(f">> 用户不存在，跳过费用检查")
        else:
            # 如果用户数据库不可用，跳过费用检查
            search_cost = 0
            print(f">> 用户数据库不可用，跳过费用检查")

        if agent:
            # 使用真实的代理，添加严格超时控制
            print(f">> 代理可用，开始快速搜索")
            try:
                if request.rawQuery:  # TODO
                    # Use natural language processing with timeout
                    results = await asyncio.wait_for(
                        agent.conduct_literature_review(
                            raw_query=request.rawQuery,
                            # max_papers=min(request.maxPapers, 5),  # 限制数量
                            max_papers=max(request.maxPapers, 5),
                            sources=request.sources,
                            retrieve_full_text=request.retrieveFullText,  # 强制关闭全文检索
                            year_start=request.yearStart,
                            year_end=request.yearEnd,
                        ),
                        timeout=300,  # 300秒总超时，给AI和外部API足够时间
                    )
                else:
                    # Use legacy structured query with timeout
                    results = await asyncio.wait_for(
                        agent.conduct_literature_review(
                            research_topic=request.query,
                            # max_papers=min(request.maxPapers, 5),  # 限制数量
                            max_papers=max(request.maxPapers, 5),
                            sources=request.sources,
                            retrieve_full_text=request.retrieveFullText,  # 强制关闭全文检索
                            year_start=request.yearStart,
                            year_end=request.yearEnd,
                        ),
                        timeout=300,  # 300秒总超时，给AI和外部API足够时间
                    )
            except asyncio.TimeoutError:
                print(">> 搜索超时，返回超时响应")
                # 返回超时响应而不是抛出异常
                results = {
                    "processed_papers": [],
                    "action_plan": [
                        f"🔍 搜索查询：{query_to_use}",
                        "⏰ 搜索超时",
                        "🔄 请稍后重试",
                        "💡 建议：使用更简单的关键词",
                    ],
                }

            # print(f">> 代理返回结果: {type(results)}")
            print(
                f">> 结果键: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}"
            )

            # 转换结果格式
            papers = []
            action_plan = None

            if results and "processed_papers" in results:
                print(
                    f">> 找到 processed_papers，数量: {len(results['processed_papers'])}"
                )
                for paper_data in results["processed_papers"]:
                    paper = Paper(
                        title=paper_data.get("title", "未知标题"),
                        authors=paper_data.get("authors", []),
                        publishedDate=paper_data.get("published_date", ""),
                        source=paper_data.get("source", "unknown"),
                        summary=paper_data.get(
                            "ai_enhanced_summary", paper_data.get("summary", "")
                        ),
                        keywords=paper_data.get("keywords", []),
                        url=paper_data.get("url", ""),
                        pdfUrl=paper_data.get("pdf_url", ""),
                        fullTextRetrieved=paper_data.get("full_text_retrieved", False),
                    )
                    papers.append(paper)

                # Extract action plan from results
                action_plan = results.get("action_plan", [])
            else:
                print(f">> 未找到 processed_papers 或结果为空")
                print(f">> 完整结果: {results}")
        else:
            # Agent not available - return error instead of mock data
            raise HTTPException(
                status_code=503,
                detail="Literature agent is not available. Please check system configuration and ensure all required services are running.",
            )

        processing_time = time.time() - start_time

        print(f"检索完成: 找到 {len(papers)} 篇论文，耗时 {processing_time:.2f}s")

        # 扣费逻辑
        if user_db and search_cost > 0:
            with user_db.get_db() as db:
                real_user = user_db.get_user_by_username(db, current_user.username)
                if real_user:
                    success = user_db.deduct_balance(
                        real_user.id, search_cost, len(papers), query_to_use
                    )
                    if success:
                        print(f">> 扣费成功：{search_cost:.2f}元")
                    else:
                        print(f">> 扣费失败，但搜索已成功完成")
                else:
                    print(f">> 用户不存在，无法扣费")

        return SearchResult(
            papers=papers,
            totalCount=len(papers),
            processingTime=processing_time,
            summary=f"基于'{query_to_use}'的文献检索完成，共找到{len(papers)}篇相关论文。",
            actionPlan=action_plan,
        )

    except Exception as e:
        print(f"检索失败: {e}")
        raise HTTPException(status_code=500, detail=f"检索失败: {str(e)}")


@app.post("/api/generate-report")
@rate_limit_api
async def generate_report(
    request: ReportRequest, current_user: AuthUser = Depends(get_current_active_user)
):
    """生成综述报告"""
    try:
        print(f"开始生成报告: {request.title}")

        agent = get_agent()
        if not agent:
            raise HTTPException(
                status_code=503,
                detail="Literature agent is not available for report generation",
            )

        # 使用真实的agent生成报告
        try:
            # 转换paper数据格式以便agent处理
            papers_data = []
            for paper in request.papers:
                # 处理paper可能是字典或对象的情况
                if isinstance(paper, dict):
                    paper_dict = paper
                else:
                    paper_dict = {
                        "title": getattr(paper, "title", ""),
                        "authors": getattr(paper, "authors", []),
                        "publishedDate": getattr(paper, "publishedDate", ""),
                        "source": getattr(paper, "source", ""),
                        "summary": getattr(paper, "summary", ""),
                        "keywords": getattr(paper, "keywords", []),
                        "url": getattr(paper, "url", ""),
                        "fullTextRetrieved": getattr(paper, "fullTextRetrieved", False),
                    }

                papers_data.append(
                    {
                        "id": paper_dict.get("id", f"paper_{len(papers_data)}"),
                        "title": paper_dict.get("title", ""),
                        "authors": paper_dict.get("authors", []),
                        "published_date": paper_dict.get("publishedDate", ""),
                        "source": paper_dict.get("source", ""),
                        "summary": paper_dict.get("summary", ""),
                        "keywords": paper_dict.get("keywords", []),
                        "url": paper_dict.get("url", ""),
                        "pdf_url": paper_dict.get("pdfUrl", ""),
                        "full_text_retrieved": paper_dict.get(
                            "fullTextRetrieved", False
                        ),
                    }
                )

            # 调用agent的报告生成功能
            report_result = await agent.generate_full_report(
                papers=papers_data, topic=request.title, output_format="markdown"
            )

            report = (
                report_result.get("content", "")
                if isinstance(report_result, dict)
                else str(report_result)
            )

            if not report.strip():
                raise HTTPException(status_code=500, detail="Generated report is empty")

            print("报告生成完成")
            return {"report": report}

        except Exception as e:
            print(f"Agent报告生成异常: {e}")
            raise HTTPException(
                status_code=500, detail=f"Report generation failed: {str(e)}"
            )

    except Exception as e:
        print(f"报告生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")


# 支付相关API
class RechargeRequest(BaseModel):
    """充值请求模型."""

    amount: float
    payment_method: str = "alipay"


class RechargeResponse(BaseModel):
    """充值响应模型."""

    success: bool
    message: str
    order_id: Optional[str] = None
    qr_code_path: Optional[str] = None


@app.get("/api/user/balance")
async def get_user_balance(current_user: AuthUser = Depends(get_current_active_user)):
    """获取用户余额信息."""
    if not user_db:
        raise HTTPException(status_code=503, detail="用户服务不可用")

    with user_db.get_db() as db:
        real_user = user_db.get_user_by_username(db, current_user.username)
        if not real_user:
            raise HTTPException(status_code=404, detail="用户不存在")

    balance_info = user_db.get_user_balance(real_user.id)
    if not balance_info:
        raise HTTPException(status_code=500, detail="获取余额信息失败")

    return balance_info


@app.get("/api/user/usage-history")
async def get_usage_history(
    limit: int = 50, current_user: AuthUser = Depends(get_current_active_user)
):
    """获取用户使用历史."""
    if not user_db:
        raise HTTPException(status_code=503, detail="用户服务不可用")

    with user_db.get_db() as db:
        real_user = user_db.get_user_by_username(db, current_user.username)
        if not real_user:
            raise HTTPException(status_code=404, detail="用户不存在")

    return user_db.get_usage_history(real_user.id, limit)


@app.get("/api/user/recharge-history")
async def get_recharge_history(
    limit: int = 50, current_user: AuthUser = Depends(get_current_active_user)
):
    """获取用户充值历史."""
    if not user_db:
        raise HTTPException(status_code=503, detail="用户服务不可用")

    with user_db.get_db() as db:
        real_user = user_db.get_user_by_username(db, current_user.username)
        if not real_user:
            raise HTTPException(status_code=404, detail="用户不存在")

    return user_db.get_recharge_history(real_user.id, limit)


@app.post("/api/payment/recharge", response_model=RechargeResponse)
async def create_recharge_order(
    request: RechargeRequest, current_user: AuthUser = Depends(get_current_active_user)
):
    """创建充值订单."""
    if not user_db:
        raise HTTPException(status_code=503, detail="用户服务不可用")

    # 验证充值金额
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="充值金额必须大于0")

    # 预定义的充值金额选项
    valid_amounts = [10, 50, 100, 200]
    if request.amount not in valid_amounts:
        raise HTTPException(
            status_code=400, detail=f"充值金额必须是以下选项之一: {valid_amounts}"
        )

    with user_db.get_db() as db:
        real_user = user_db.get_user_by_username(db, current_user.username)
        if not real_user:
            raise HTTPException(status_code=404, detail="用户不存在")

    # 生成订单ID
    order_id = f"recharge_{real_user.id}_{int(datetime.now().timestamp())}"

    # 这里简化处理，直接返回收款码路径
    # 实际项目中应该集成支付宝SDK创建订单
    qr_code_path = "/Users/gengyx/Documents/博士2025-2029/文献综述/AI-Agent-for-Automated-Literature-Review-Summarization/media/收款码zfb.jpg"

    return RechargeResponse(
        success=True,
        message=f"请扫码支付{request.amount}元",
        order_id=order_id,
        qr_code_path=qr_code_path,
    )


@app.post("/api/payment/confirm")
async def confirm_payment(
    order_id: str, current_user: AuthUser = Depends(get_current_active_user)
):
    """确认支付完成（简化版本）."""
    if not user_db:
        raise HTTPException(status_code=503, detail="用户服务不可用")

    # 解析订单ID获取金额
    try:
        parts = order_id.split("_")
        if len(parts) != 3 or parts[0] != "recharge":
            raise ValueError("Invalid order ID format")

        user_id = int(parts[1])
        amount = float(parts[2])  # 在实际项目中，应该从数据库查询订单金额
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="无效的订单ID")

    with user_db.get_db() as db:
        real_user = user_db.get_user_by_username(db, current_user.username)
        if not real_user or real_user.id != user_id:
            raise HTTPException(status_code=404, detail="用户不存在")

    # 执行充值
    success = user_db.add_balance(real_user.id, amount, "alipay", order_id)
    if success:
        return {"success": True, "message": f"充值成功，已到账{amount}元"}
    else:
        return {"success": False, "message": "充值失败"}


if __name__ == "__main__":
    import uvicorn

    print("启动 FastAPI 服务器...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="info")
