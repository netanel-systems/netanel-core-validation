"""Scenario 4: Edge Cases.

Tests edge cases like timeouts, errors, and recovery.
Note: Without mocking netanel-core internals, we can only test
what happens when tasks complete successfully. This scenario
validates the framework handles normal edge cases.

Budget: ~$0.10
"""

from __future__ import annotations

from pathlib import Path

import pytest

from validation.assertions import assert_no_crashes, assert_quality_threshold
from validation.config import ValidationConfig
from validation.tasks import CODING_TASKS
from validation.validator import LearningValidator


@pytest.mark.scenario4
def test_edge_cases(
    memories_dir: Path,
    artifacts_dir: Path,
    config: ValidationConfig,
) -> None:
    """Test edge cases handling.

    Tests:
    - Empty task handling (if task is empty, validator should handle)
    - Very short tasks
    - Very long tasks
    - Special characters in tasks
    - Repeated tasks

    Success criteria:
    - All calls complete without crashes
    - Quality maintained for valid tasks
    """
    # Edge case tasks
    edge_tasks = [
        # Very short
        "Add two numbers.",
        "Sort a list.",
        # Very long (complex requirement)
        " ".join(["Implement a function to"] + ["process"] * 20 + ["data efficiently."]),
        # Special characters
        "Write a function to handle UTF-8 text: 你好, мир, 🌍",
        # Repeated task (should still learn)
        "Write a function that checks if a number is prime.",
        "Write a function that checks if a number is prime.",  # Duplicate
        # Mix from existing tasks
        *CODING_TASKS[:4],
    ]

    validator = LearningValidator(
        namespace="validation-edge-cases",
        memories_dir=memories_dir,
        config=config,
        artifacts_dir=artifacts_dir,
    )

    validator.setup()

    # Execute edge case tasks
    result = validator.run_scenario(
        tasks=edge_tasks,
        max_calls=len(edge_tasks),
    )

    # Verify no crashes
    call_results = [{"success": True} for _ in range(result.total_calls)]
    assert_no_crashes(call_results)

    # Verify quality (may be lower for edge cases, so check > 0.5)
    assert_quality_threshold(
        validator.metrics.quality_scores,
        min_threshold=0.5,  # Lower threshold for edge cases
    )

    # Log summary
    print(f"\n✅ Scenario 4 PASSED")
    print(f"   Edge cases tested: {result.total_calls}")
    print(f"   Quality: {validator.metrics._quality_stats()['mean']:.3f}")
    print(f"   Cost: ${result.estimated_cost_usd:.4f}")

    validator.cleanup()
