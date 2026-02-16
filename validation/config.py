"""Validation configuration using Pydantic settings.

Provides flexible configuration for quality thresholds, cost limits,
timeouts, and retry policies without hardcoding values.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ValidationConfig(BaseSettings):
    """Configuration for validation framework.

    All settings can be overridden via environment variables with
    VALIDATION_ prefix (e.g., VALIDATION_QUALITY_THRESHOLD=0.8).
    """

    model_config = SettingsConfigDict(
        env_prefix="VALIDATION_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
    )

    # Quality thresholds
    quality_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum acceptable quality score for LLM responses",
    )

    # Cost limits
    max_cost_usd: float = Field(
        default=1.00,
        ge=0.0,
        description="Maximum allowed cost in USD for validation runs",
    )

    # Timeouts
    timeout_seconds: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Timeout in seconds for individual LLM calls",
    )

    # Retry policy
    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum number of retries for failed LLM calls",
    )

    retry_delay_seconds: int = Field(
        default=5,
        ge=1,
        le=60,
        description="Delay in seconds between retries",
    )

    # Memory cleanup
    cleanup_memories: bool = Field(
        default=True,
        description="Whether to clean up memory directories after scenarios",
    )

    # Artifact settings
    save_artifacts: bool = Field(
        default=True,
        description="Whether to save validation artifacts (logs, snapshots)",
    )

    artifacts_dir: str = Field(
        default="artifacts",
        description="Directory to store validation artifacts",
    )
