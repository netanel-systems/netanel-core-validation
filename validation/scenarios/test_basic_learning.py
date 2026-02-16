"""Scenario 1: Basic Learning Loop.

Tests core learning pipeline with 10 real LLM calls.
Verifies quality, memory persistence, and learning extraction.

Budget: ~$0.10 (buffer for safety)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from validation import (
    assert_cost_within_budget,
    assert_learning_extracted,
    assert_memory_persisted,
    assert_quality_threshold,
)
from validation.config import ValidationConfig
from validation.tasks import CODING_TASKS
from validation.validator import LearningValidator


@pytest.mark.scenario1
def test_basic_learning_loop(
    memories_dir: Path,
    artifacts_dir: Path,
    config: ValidationConfig,
) -> None:
    """Test basic learning loop with 10 LLM calls.

    Success criteria:
    - All 10 calls complete successfully
    - Quality scores >= 0.7
    - Memory persists (patterns stored)
    - Learnings extracted from responses
    """
    # Setup validator
    validator = LearningValidator(
        namespace="validation-basic",
        memories_dir=memories_dir,
        config=config,
        artifacts_dir=artifacts_dir,
    )

    # Capture initial memory snapshot
    validator.setup()
    initial_snapshot = validator.metrics.snapshots[-1]

    # Execute 10 tasks
    result = validator.run_scenario(
        tasks=CODING_TASKS[:10],
        max_calls=10,
    )

    # Assertions
    assert result.success, f"Validation failed: {result.error}"
    assert result.total_calls == 10, f"Expected 10 calls, got {result.total_calls}"

    # Verify quality threshold
    quality_scores = validator.metrics.quality_scores
    assert_quality_threshold(quality_scores, min_threshold=config.quality_threshold)

    # Verify memory persisted
    final_snapshot = validator.metrics.snapshots[-1]
    assert_memory_persisted(initial_snapshot, final_snapshot)

    # Verify learnings extracted
    assert_learning_extracted(final_snapshot, min_patterns=1)

    # Verify budget
    assert_cost_within_budget(result.estimated_cost_usd, max_budget=0.10)

    # Log summary
    quality_stats = validator.metrics._quality_stats()
    mean_quality = quality_stats.get("mean", 0.0)

    print("\n✅ Scenario 1 PASSED")
    print(f"   Calls: {result.total_calls}")
    print(f"   Quality: {mean_quality:.3f}")
    print(f"   Cost: ${result.estimated_cost_usd:.4f}")
    print(f"   Memory growth: {final_snapshot.total_files - initial_snapshot.total_files} files")

    # Cleanup
    validator.cleanup()
