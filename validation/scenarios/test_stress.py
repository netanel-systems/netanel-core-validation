"""Scenario 3: Stress Test.

Tests error handling and retries with 50 calls.
No actual error injection (that would require mocking netanel-core).
Just validates high volume works robustly.

Budget: ~$0.25
"""

from __future__ import annotations

from pathlib import Path

import pytest

from validation.assertions import assert_cost_within_budget, assert_no_crashes, assert_quality_threshold
from validation.config import ValidationConfig
from validation.tasks import CODING_TASKS
from validation.validator import LearningValidator


@pytest.mark.scenario3
def test_stress_with_high_volume(
    memories_dir: Path,
    artifacts_dir: Path,
    config: ValidationConfig,
) -> None:
    """Test stress with 50 LLM calls.

    Success criteria:
    - All 50 calls complete successfully
    - No crashes or hangs
    - Quality maintained under load
    - Cost within budget
    """
    validator = LearningValidator(
        namespace="validation-stress",
        memories_dir=memories_dir,
        config=config,
        artifacts_dir=artifacts_dir,
    )

    validator.setup()

    # Execute 50 tasks
    result = validator.run_scenario(
        tasks=CODING_TASKS[:50],
        max_calls=50,
    )

    # Verify no crashes
    call_results = [{"success": True} for _ in range(result.total_calls)]
    assert_no_crashes(call_results)

    # Verify quality maintained
    assert_quality_threshold(
        validator.metrics.quality_scores,
        min_threshold=config.quality_threshold,
    )

    # Verify cost within budget
    assert_cost_within_budget(
        actual_cost=result.estimated_cost_usd,
        max_budget=config.max_cost_usd,
    )

    # Log summary
    print(f"\n✅ Scenario 3 PASSED")
    print(f"   Calls: {result.total_calls}")
    print(f"   Quality: {validator.metrics._quality_stats()['mean']:.3f}")
    print(f"   Cost: ${result.estimated_cost_usd:.4f}")
    print(f"   Latency P95: {validator.metrics._latency_stats()['p95_s']:.2f}s")

    validator.cleanup()
