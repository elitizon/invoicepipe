"""Configuration management for invoice extractor."""

import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings."""
    
    # AI Provider Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash-exp", env="GEMINI_MODEL")
    
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")
    
    # File Processing
    supported_formats: list[str] = ["pdf", "png", "jpg", "jpeg"]
    max_file_size_mb: int = Field(default=10, env="MAX_FILE_SIZE_MB")
    
    @property
    def has_ai_provider(self) -> bool:
        """Check if at least one AI provider is configured."""
        return bool(self.openai_api_key or self.gemini_api_key or self.anthropic_api_key)
    
    def get_preferred_model(self) -> tuple[str, str]:
        """Get the preferred AI model and API key."""
        if self.openai_api_key:
            return self.openai_model, self.openai_api_key
        elif self.gemini_api_key:
            return self.gemini_model, self.gemini_api_key
        elif self.anthropic_api_key:
            return self.anthropic_model, self.anthropic_api_key
        else:
            raise ValueError("No AI provider configured")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
