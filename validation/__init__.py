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
    assert_cost_within_budget,
    assert_evolution_triggered,
    assert_learning_extracted,
    assert_memory_persisted,
    assert_no_crashes,
    assert_quality_threshold,
)

__all__ = [
    "ArtifactManager",
    "LearningValidator",
    "MemorySnapshot",
    "MetricsCollector",
    "ValidationConfig",
    "ValidationResult",
    "assert_cost_within_budget",
    "assert_evolution_triggered",
    "assert_learning_extracted",
    "assert_memory_persisted",
    "assert_no_crashes",
    "assert_quality_threshold",
]
