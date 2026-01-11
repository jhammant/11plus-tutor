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

    # Learning Features - Free tier
    enable_topic_lessons: bool = True      # Topic explanations & worked examples
    enable_strategy_guides: bool = True    # How-to guides for question types
    enable_learning_paths_view: bool = True # View learning paths (read-only)

    # ===================
    # Feature Flags - Paid Only
    # ===================
    enable_ai_tutor: bool = False          # AI tutor chat (explain concepts)
    enable_ai_generation: bool = False     # Generate new questions with AI
    enable_advanced_analytics: bool = False # Detailed analytics & predictions
    enable_adaptive_difficulty: bool = False # Auto-adjust difficulty
    enable_parent_dashboard: bool = False  # Multi-student tracking
    enable_cloud_sync: bool = False        # Sync progress to cloud

    # Learning Features - Paid tier
    enable_ai_explanations: bool = False   # AI-generated detailed explanations
    enable_learning_path_progress: bool = False # Track progress through paths
    enable_unlimited_examples: bool = False # Unlimited worked examples
    enable_oak_videos: bool = False        # Oak National Academy videos

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
            # Core features (always on)
            "practice_mode": self.enable_practice_mode,
            "mock_exams": self.enable_mock_exams,
            "progress_tracking": self.enable_progress_tracking,
            "achievements": self.enable_achievements,
            # Learning features (free tier)
            "topic_lessons": self.enable_topic_lessons,
            "strategy_guides": self.enable_strategy_guides,
            "learning_paths_view": self.enable_learning_paths_view,
            # Paid features
            "ai_tutor": self.enable_ai_tutor and self.is_paid_mode(),
            "ai_generation": self.enable_ai_generation and self.is_paid_mode(),
            "advanced_analytics": self.enable_advanced_analytics and self.is_paid_mode(),
            "adaptive_difficulty": self.enable_adaptive_difficulty and self.is_paid_mode(),
            "parent_dashboard": self.enable_parent_dashboard and self.is_paid_mode(),
            "cloud_sync": self.enable_cloud_sync and self.is_paid_mode(),
            # Paid learning features
            "ai_explanations": self.enable_ai_explanations and self.is_paid_mode(),
            "learning_path_progress": self.enable_learning_path_progress and self.is_paid_mode(),
            "unlimited_examples": self.enable_unlimited_examples and self.is_paid_mode(),
            "oak_videos": self.enable_oak_videos and self.is_paid_mode(),
            # Meta
            "is_paid": self.is_paid_mode(),
        }


settings = Settings()
