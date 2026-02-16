"""Metrics collection for validation runs.

Tracks performance and quality metrics:
- Latency (response time per LLM call)
- Quality scores (distribution, statistics)
- Memory growth (files, patterns, evolutions)
- Cost (API tokens, estimated USD)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class MemorySnapshot:
    """Snapshot of memory state at a point in time.

    Used to track memory growth between validation runs.
    """

    timestamp: float
    total_files: int
    total_size_bytes: int
    pattern_count: int = 0
    evolution_count: int = 0

    @classmethod
    def capture(cls, memories_dir: Path) -> MemorySnapshot:
        """Capture current state of memory directory.

        Args:
            memories_dir: Path to memories directory.

        Returns:
            MemorySnapshot with current state.
        """
        if not memories_dir.exists():
            return cls(
                timestamp=time.time(),
                total_files=0,
                total_size_bytes=0,
            )

        files = list(memories_dir.rglob("*"))
        total_files = 0
        total_size = 0
        for f in files:
            if f.is_file():
                total_files += 1
                total_size += f.stat().st_size

        # Count patterns and evolutions (if netanel-core creates these files)
        pattern_count = len(list(memories_dir.glob("**/patterns.jsonl")))
        evolution_count = len(list(memories_dir.glob("**/evolutions.jsonl")))

        return cls(
            timestamp=time.time(),
            total_files=total_files,
            total_size_bytes=total_size,
            pattern_count=pattern_count,
            evolution_count=evolution_count,
        )


@dataclass
class MetricsCollector:
    """Collect and analyze validation metrics.

    Tracks all performance and quality metrics for a validation run.
    """

    # Latency tracking
    call_durations: list[float] = field(default_factory=list)

    # Quality tracking
    quality_scores: list[float] = field(default_factory=list)

    # Cost tracking (estimated)
    total_tokens: int = 0
    total_calls: int = 0

    # Memory snapshots
    snapshots: list[MemorySnapshot] = field(default_factory=list)

    def record_call(
        self,
        duration_s: float,
        quality_score: float,
        tokens_used: int = 0,
    ) -> None:
        """Record metrics for a single LLM call.

        Args:
            duration_s: Call duration in seconds.
            quality_score: Quality score (0.0-1.0).
            tokens_used: Number of tokens consumed.
        """
        self.call_durations.append(duration_s)
        self.quality_scores.append(quality_score)
        self.total_tokens += tokens_used
        self.total_calls += 1

    def snapshot_memory(self, memories_dir: Path) -> MemorySnapshot:
        """Capture and store memory snapshot.

        Args:
            memories_dir: Path to memories directory.

        Returns:
            MemorySnapshot with current state.
        """
        snapshot = MemorySnapshot.capture(memories_dir)
        self.snapshots.append(snapshot)
        return snapshot

    def export(self) -> dict[str, Any]:
        """Export all collected metrics.

        Returns:
            Dictionary with all metrics and statistics.
        """
        return {
            "total_calls": self.total_calls,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": self._estimate_cost(),
            "latency": self._latency_stats(),
            "quality": self._quality_stats(),
            "memory": self._memory_stats(),
        }

    def _estimate_cost(self) -> float:
        """Estimate total cost in USD.

        Uses gpt-4o-mini pricing: $0.15/1M input, $0.60/1M output.
        Assumes 50/50 split for simplicity.

        Returns:
            Estimated cost in USD.
        """
        if self.total_tokens == 0:
            return 0.0

        # Average price: ($0.15 + $0.60) / 2 = $0.375 per 1M tokens
        avg_price_per_million = 0.375
        return (self.total_tokens / 1_000_000) * avg_price_per_million

    def _latency_stats(self) -> dict[str, float]:
        """Calculate latency statistics.

        Returns:
            Dict with min, max, mean, p50, p95, p99 latencies.
        """
        if not self.call_durations:
            return {}

        sorted_durations = sorted(self.call_durations)
        n = len(sorted_durations)

        def percentile_index(p: float, count: int) -> int:
            """Calculate nearest-rank percentile index."""
            import math

            return min(max(0, math.ceil(p * count) - 1), count - 1)

        return {
            "min_s": sorted_durations[0],
            "max_s": sorted_durations[-1],
            "mean_s": sum(sorted_durations) / n,
            "p50_s": sorted_durations[percentile_index(0.50, n)],
            "p95_s": sorted_durations[percentile_index(0.95, n)],
            "p99_s": sorted_durations[percentile_index(0.99, n)],
        }

    def _quality_stats(self) -> dict[str, float]:
        """Calculate quality score statistics.

        Returns:
            Dict with min, max, mean, std dev of quality scores.
        """
        if not self.quality_scores:
            return {}

        n = len(self.quality_scores)
        mean = sum(self.quality_scores) / n
        variance = sum((x - mean) ** 2 for x in self.quality_scores) / n
        std_dev = variance**0.5

        return {
            "min": min(self.quality_scores),
            "max": max(self.quality_scores),
            "mean": mean,
            "std_dev": std_dev,
        }

    def _memory_stats(self) -> dict[str, Any]:
        """Calculate memory growth statistics.

        Returns:
            Dict with initial, final, and growth metrics.
        """
        if len(self.snapshots) < 2:
            return {}

        initial = self.snapshots[0]
        final = self.snapshots[-1]

        return {
            "initial_files": initial.total_files,
            "final_files": final.total_files,
            "files_created": final.total_files - initial.total_files,
            "initial_size_bytes": initial.total_size_bytes,
            "final_size_bytes": final.total_size_bytes,
            "size_growth_bytes": final.total_size_bytes - initial.total_size_bytes,
            "patterns_created": final.pattern_count - initial.pattern_count,
            "evolutions_triggered": final.evolution_count - initial.evolution_count,
        }
