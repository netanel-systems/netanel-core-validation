"""Validation assertions for quality enforcement.

Provides assertion functions to verify validation success criteria:
- Quality thresholds met
- Memory persisted correctly
- No crashes occurred
- Learnings extracted
"""

from __future__ import annotations

from validation.metrics import MemorySnapshot


def assert_quality_threshold(scores: list[float], min_threshold: float = 0.7) -> None:
    """Assert all quality scores meet minimum threshold.

    Args:
        scores: List of quality scores (0.0-1.0).
        min_threshold: Minimum acceptable score.

    Raises:
        AssertionError: If any score is below threshold.
    """
    if not scores:
        raise AssertionError("No quality scores to validate")

    below_threshold = [s for s in scores if s < min_threshold]

    if below_threshold:
        failures = len(below_threshold)
        total = len(scores)
        min_score = min(scores)
        raise AssertionError(
            f"{failures}/{total} calls below quality threshold {min_threshold:.2f}. "
            f"Minimum score: {min_score:.3f}"
        )


def assert_memory_persisted(before: MemorySnapshot, after: MemorySnapshot) -> None:
    """Assert memory persisted and grew.

    Args:
        before: Memory snapshot before validation.
        after: Memory snapshot after validation.

    Raises:
        AssertionError: If memory did not persist or grow.
    """
    if after.total_files <= before.total_files:
        raise AssertionError(
            f"Memory did not grow. Before: {before.total_files} files, "
            f"After: {after.total_files} files"
        )

    if after.total_size_bytes <= before.total_size_bytes:
        raise AssertionError(
            f"Memory size did not grow. Before: {before.total_size_bytes} bytes, "
            f"After: {after.total_size_bytes} bytes"
        )


def assert_no_crashes(call_results: list[dict]) -> None:
    """Assert no crashes or failures occurred.

    Args:
        call_results: List of call result dicts with 'success' field.

    Raises:
        AssertionError: If any calls crashed or failed.
    """
    if not call_results:
        raise AssertionError("No call results to validate")

    failures = [r for r in call_results if not r.get("success", False)]

    if failures:
        count = len(failures)
        total = len(call_results)
        raise AssertionError(
            f"{count}/{total} calls crashed or failed. "
            f"First failure: {failures[0].get('error', 'Unknown error')}"
        )


def assert_learning_extracted(snapshot: MemorySnapshot, min_patterns: int = 1) -> None:
    """Assert learnings were extracted and stored.

    Args:
        snapshot: Memory snapshot after validation.
        min_patterns: Minimum number of patterns expected.

    Raises:
        AssertionError: If no learnings were extracted.
    """
    if snapshot.pattern_count < min_patterns:
        raise AssertionError(
            f"Insufficient learnings extracted. Expected >= {min_patterns}, "
            f"got {snapshot.pattern_count}"
        )


def assert_evolution_triggered(before: MemorySnapshot, after: MemorySnapshot) -> None:
    """Assert prompt evolution was triggered.

    Args:
        before: Memory snapshot before validation.
        after: Memory snapshot after validation.

    Raises:
        AssertionError: If evolution did not trigger.
    """
    evolutions_triggered = after.evolution_count - before.evolution_count

    if evolutions_triggered < 1:
        raise AssertionError(
            f"Evolution did not trigger. Before: {before.evolution_count}, "
            f"After: {after.evolution_count}"
        )


def assert_cost_within_budget(actual_cost: float, max_budget: float) -> None:
    """Assert actual cost is within budget.

    Args:
        actual_cost: Actual cost in USD.
        max_budget: Maximum allowed budget in USD.

    Raises:
        AssertionError: If cost exceeds budget.
    """
    if actual_cost > max_budget:
        raise AssertionError(
            f"Cost exceeded budget. Budget: ${max_budget:.2f}, "
            f"Actual: ${actual_cost:.2f}"
        )
