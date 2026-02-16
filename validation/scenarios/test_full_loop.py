"""Scenario 2: Full Loop with Evolution.

Tests prompt evolution and session restart with 30 calls.
Verifies evolution triggers and memory survives restart.

Budget: ~$0.15
"""

from __future__ import annotations

from pathlib import Path

import pytest

from validation import assert_evolution_triggered, assert_memory_persisted
from validation.assertions import assert_quality_threshold
from validation.config import ValidationConfig
from validation.tasks import CODING_TASKS
from validation.validator import LearningValidator


@pytest.mark.scenario2
def test_full_loop_with_evolution(
    memories_dir: Path,
    artifacts_dir: Path,
    config: ValidationConfig,
) -> None:
    """Test full loop with evolution across 30 calls + session restart.

    Success criteria:
    - Evolution triggers after ~10-15 calls
    - Prompt updated in memory
    - Memory survives session restart
    - Evolved prompt used in resumed session
    """
    # Phase 1: Run 30 calls to trigger evolution
    validator1 = LearningValidator(
        namespace="validation-evolution",
        memories_dir=memories_dir,
        config=config,
        artifacts_dir=artifacts_dir,
    )

    validator1.setup()
    initial_snapshot = validator1.metrics.snapshots[-1]

    result1 = validator1.run_scenario(
        tasks=CODING_TASKS[:30],
        max_calls=30,
    )

    mid_snapshot = validator1.metrics.snapshots[-1]

    # Verify evolution triggered
    assert_evolution_triggered(initial_snapshot, mid_snapshot)

    validator1.cleanup()

    # Phase 2: Restart session with same memories_dir
    validator2 = LearningValidator(
        namespace="validation-evolution",
        memories_dir=memories_dir,  # Same directory
        config=config,
        artifacts_dir=artifacts_dir,
    )

    validator2.setup()
    restart_snapshot = validator2.metrics.snapshots[-1]

    # Verify memory survived restart
    assert_memory_persisted(initial_snapshot, restart_snapshot)

    # Run 10 more calls with evolved prompt
    result2 = validator2.run_scenario(
        tasks=CODING_TASKS[30:40],
        max_calls=10,
    )

    final_snapshot = validator2.metrics.snapshots[-1]

    # Verify quality maintained
    all_scores = validator1.metrics.quality_scores + validator2.metrics.quality_scores
    assert_quality_threshold(all_scores, min_threshold=config.quality_threshold)

    # Log summary
    total_cost = result1.estimated_cost_usd + result2.estimated_cost_usd
    print(f"\n✅ Scenario 2 PASSED")
    print(f"   Phase 1 calls: {result1.total_calls}")
    print(f"   Phase 2 calls: {result2.total_calls}")
    print(f"   Evolution triggered: {mid_snapshot.evolution_count - initial_snapshot.evolution_count}")
    print(f"   Total cost: ${total_cost:.4f}")

    validator2.cleanup()
