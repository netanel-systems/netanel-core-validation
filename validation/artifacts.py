"""Artifact management for validation outputs.

Saves validation artifacts for inspection:
- Logs (full LLM call history)
- Memory snapshots (before/after states)
- Metrics (JSON export of all statistics)
- Reports (human-readable summaries)
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from validation.metrics import MemorySnapshot


class ArtifactManager:
    """Manage validation artifacts.

    Saves logs, snapshots, metrics, and reports to artifacts directory.
    """

    def __init__(self, artifacts_dir: Path | None) -> None:
        """Initialize artifact manager.

        Args:
            artifacts_dir: Directory to save artifacts. If None, artifacts are disabled.
        """
        self.artifacts_dir = artifacts_dir
        self._enabled = artifacts_dir is not None

        if self._enabled and not artifacts_dir.exists():
            artifacts_dir.mkdir(parents=True, exist_ok=True)

    def save_log(self, call_index: int, call_data: dict[str, Any]) -> None:
        """Save log entry for a single LLM call.

        Args:
            call_index: Index of this call (0-based).
            call_data: Dict with task, response, quality_score, duration_s, etc.
        """
        if not self._enabled:
            return

        log_file = self.artifacts_dir / "calls.jsonl"

        entry = {
            "call_index": call_index,
            "timestamp": datetime.now().isoformat(),
            **call_data,
        }

        with log_file.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def save_snapshot(self, name: str, snapshot: MemorySnapshot) -> None:
        """Save memory snapshot.

        Args:
            name: Snapshot name (e.g., "initial", "final", "after_evolution").
            snapshot: MemorySnapshot to save.
        """
        if not self._enabled:
            return

        snapshots_dir = self.artifacts_dir / "snapshots"
        snapshots_dir.mkdir(exist_ok=True)

        snapshot_file = snapshots_dir / f"{name}.json"
        snapshot_file.write_text(json.dumps(asdict(snapshot), indent=2))

    def save_metrics(self, metrics: dict[str, Any]) -> None:
        """Save metrics export.

        Args:
            metrics: Metrics dictionary (from MetricsCollector.export()).
        """
        if not self._enabled:
            return

        metrics_file = self.artifacts_dir / "metrics.json"
        metrics_file.write_text(json.dumps(metrics, indent=2))

    def generate_report(self, metrics: dict[str, Any]) -> str:
        """Generate human-readable validation report.

        Args:
            metrics: Metrics dictionary.

        Returns:
            Markdown-formatted report.
        """
        if not metrics:
            return "No metrics available"

        report_lines = [
            "# Validation Report",
            "",
            f"**Generated:** {datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"- **Total Calls:** {metrics.get('total_calls', 0)}",
            f"- **Total Tokens:** {metrics.get('total_tokens', 0):,}",
            f"- **Estimated Cost:** ${metrics.get('estimated_cost_usd', 0):.4f}",
            "",
        ]

        # Latency
        if latency := metrics.get("latency"):
            report_lines.extend([
                "## Latency",
                "",
                f"- **Min:** {latency.get('min_s', 0):.2f}s",
                f"- **Max:** {latency.get('max_s', 0):.2f}s",
                f"- **Mean:** {latency.get('mean_s', 0):.2f}s",
                f"- **P95:** {latency.get('p95_s', 0):.2f}s",
                "",
            ])

        # Quality
        if quality := metrics.get("quality"):
            report_lines.extend([
                "## Quality",
                "",
                f"- **Min:** {quality.get('min', 0):.3f}",
                f"- **Max:** {quality.get('max', 0):.3f}",
                f"- **Mean:** {quality.get('mean', 0):.3f}",
                f"- **Std Dev:** {quality.get('std_dev', 0):.3f}",
                "",
            ])

        # Memory
        if memory := metrics.get("memory"):
            report_lines.extend([
                "## Memory Growth",
                "",
                f"- **Initial Files:** {memory.get('initial_files', 0)}",
                f"- **Final Files:** {memory.get('final_files', 0)}",
                f"- **Files Created:** {memory.get('files_created', 0)}",
                f"- **Size Growth:** {memory.get('size_growth_bytes', 0):,} bytes",
                f"- **Patterns Created:** {memory.get('patterns_created', 0)}",
                f"- **Evolutions Triggered:** {memory.get('evolutions_triggered', 0)}",
                "",
            ])

        report = "\n".join(report_lines)

        if self._enabled:
            report_file = self.artifacts_dir / "report.md"
            report_file.write_text(report)

        return report
