"""
ExamTutor Settings
Pydantic configuration for LLM, embedding, and content APIs
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # LLM Configuration
    llm_binding: str = "openai"  # openai, ollama
    llm_host: str = "http://localhost:1234/v1"
    llm_model: str = "local-model"
    llm_api_key: str = "lm-studio"

    # Embedding Configuration
    embedding_binding: str = "ollama"
    embedding_host: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"
    embedding_api_key: str = "ollama"

    # Oak National Academy API
    oak_api_base: str = "https://open-api.thenational.academy"
    oak_api_version: str = "v1"

    # Server Configuration
    backend_port: int = 8001
    frontend_port: int = 3782

    # Database
    database_url: str = "sqlite:///./examtutor.db"

    # Feature Flags
    enable_ai_generation: bool = True
    enable_progress_tracking: bool = True
    enable_mock_exams: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
