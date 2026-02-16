"""Netanel Core Validation Framework.

Production-grade validation suite for netanel-core library.
Tests learning algorithm, memory persistence, and prompt evolution
with real LLM calls before PyPI publication.
"""

__version__ = "0.1.0"

from validation.validator import LearningValidator, ValidationResult
from validation.config import ValidationConfig
from validation.metrics import MetricsCollector, MemorySnapshot
from validation.artifacts import ArtifactManager
from validation.assertions import (
    assert_quality_threshold,
    assert_memory_persisted,
    assert_no_crashes,
    assert_learning_extracted,
)

__all__ = [
    "LearningValidator",
    "ValidationResult",
    "ValidationConfig",
    "MetricsCollector",
    "MemorySnapshot",
    "ArtifactManager",
    "assert_quality_threshold",
    "assert_memory_persisted",
    "assert_no_crashes",
    "assert_learning_extracted",
]
