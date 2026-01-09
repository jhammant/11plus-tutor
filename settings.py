"""
11+ Tutor Settings
Pydantic configuration for LLM, embedding, and content APIs
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App Mode: "opensource" or "paid"
    # opensource = free, local LLM, all basic features
    # paid = cloud LLM, advanced analytics, AI tutor chat
    app_mode: str = "opensource"

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
    backend_port: int = 8002
    frontend_port: int = 3783

    # Database
    database_url: str = "sqlite:///./elevenplustutor.db"

    # ===================
    # Feature Flags - Opensource (always enabled)
    # ===================
    enable_practice_mode: bool = True      # Basic practice questions
    enable_mock_exams: bool = True         # Timed mock exams
    enable_progress_tracking: bool = True  # Local progress tracking
    enable_achievements: bool = True       # Gamification badges

    # ===================
    # Feature Flags - Paid Only
    # ===================
    enable_ai_tutor: bool = False          # AI tutor chat (explain concepts)
    enable_ai_generation: bool = False     # Generate new questions with AI
    enable_advanced_analytics: bool = False # Detailed analytics & predictions
    enable_adaptive_difficulty: bool = False # Auto-adjust difficulty
    enable_parent_dashboard: bool = False  # Multi-student tracking
    enable_cloud_sync: bool = False        # Sync progress to cloud

    # Usage Limits (for paid tier)
    daily_ai_questions_limit: int = 0      # 0 = unlimited (paid) or 5 (free trial)
    daily_ai_tutor_messages: int = 0       # 0 = disabled in opensource

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def is_paid_mode(self) -> bool:
        """Check if running in paid mode"""
        return self.app_mode == "paid"

    def get_enabled_features(self) -> dict:
        """Get all enabled features as a dict for frontend"""
        return {
            "practice_mode": self.enable_practice_mode,
            "mock_exams": self.enable_mock_exams,
            "progress_tracking": self.enable_progress_tracking,
            "achievements": self.enable_achievements,
            "ai_tutor": self.enable_ai_tutor and self.is_paid_mode(),
            "ai_generation": self.enable_ai_generation and self.is_paid_mode(),
            "advanced_analytics": self.enable_advanced_analytics and self.is_paid_mode(),
            "adaptive_difficulty": self.enable_adaptive_difficulty and self.is_paid_mode(),
            "parent_dashboard": self.enable_parent_dashboard and self.is_paid_mode(),
            "cloud_sync": self.enable_cloud_sync and self.is_paid_mode(),
            "is_paid": self.is_paid_mode(),
        }


settings = Settings()
