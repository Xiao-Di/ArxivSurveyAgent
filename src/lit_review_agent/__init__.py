"""
PaperSurveyAgent - AI智能文献综述与摘要生成系统
AI Literature Review & Summary Generation System

A comprehensive AI-powered literature review and summary generation system
that leverages multiple AI models and academic databases to conduct
automated literature reviews and generate high-quality research summaries.
"""

__version__ = "1.1"
__author__ = "Di"
__email__ = "di@example.com"
__description__ = "AI智能文献综述与摘要生成系统"

# Core classes and functions
from .agent import LiteratureAgent
from .exceptions import (
    LiteratureReviewError,
    ConfigurationError,
    LLMError,
    SearchError,
    ProcessingError,
    ValidationError,
    RateLimitError,
    APIError,
    DatabaseError,
    FileOperationError,
    AuthenticationError,
    OperationTimeoutError,
)

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "LiteratureAgent",
    "LiteratureReviewError",
    "ConfigurationError",
    "LLMError",
    "SearchError",
    "ProcessingError",
    "ValidationError",
    "RateLimitError",
    "APIError",
    "DatabaseError",
    "FileOperationError",
    "AuthenticationError",
    "OperationTimeoutError",
]
