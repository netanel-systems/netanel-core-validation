"""Learning validator orchestrator.

Main component that orchestrates validation runs:
- Initializes netanel-core LearningLLM
- Executes tasks sequentially
- Collects metrics
- Enforces configuration bounds
- Returns validation results
"""

from __future__ import annotations

import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from validation.artifacts import ArtifactManager
from validation.config import ValidationConfig
from validation.metrics import MetricsCollector

# netanel-core is optional for this module (only needed at runtime)
try:
    from netanel_core import CallResult, LearningLLM, MemoryStore, NathanConfig
    from netanel_core.config import EvalConfig, ModelConfig, SafetyBounds

    NETANEL_CORE_AVAILABLE = True
except ImportError:
    NETANEL_CORE_AVAILABLE = False
    # Type hints for when netanel-core is not installed
    CallResult = Any
    LearningLLM = Any
    MemoryStore = Any
    NathanConfig = Any

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation run."""

    success: bool
    total_calls: int
    total_tokens: int
    estimated_cost_usd: float
    metrics: dict[str, Any]
    error: str | None = None


class LearningValidator:
    """Orchestrate validation runs with netanel-core LearningLLM.

    Manages the full validation lifecycle:
    - Setup LearningLLM instance
    - Execute tasks
    - Collect metrics
    - Enforce bounds
    - Generate artifacts
    """

    def __init__(
        self,
        namespace: str,
        memories_dir: Path,
        config: ValidationConfig,
        artifacts_dir: Path | None = None,
    ) -> None:
        """Initialize validator.

        Args:
            namespace: Namespace for LearningLLM (e.g., "validation-basic").
            memories_dir: Directory for memory persistence.
            config: Validation configuration.
            artifacts_dir: Optional directory for saving artifacts.

        Raises:
            ImportError: If netanel-core is not installed.
        """
        if not NETANEL_CORE_AVAILABLE:
            raise ImportError(
                "netanel-core not installed. "
                "Install from: ../netanel-core or pip install netanel-core"
            )

        self.namespace = namespace
        self.memories_dir = memories_dir
        self.config = config

        self.metrics = MetricsCollector()
        self.artifacts = ArtifactManager(artifacts_dir)

        self._llm: LearningLLM | None = None
        self._store: MemoryStore | None = None

    def setup(self) -> None:
        """Setup LearningLLM instance.

        Creates netanel-core configuration and initializes LearningLLM.
        """
        nathan_config = NathanConfig(
            namespace=self.namespace,
            memories_dir=self.memories_dir,
            models=ModelConfig(
                primary_model="gpt-4o-mini",
                evaluator_model="gpt-4o-mini",
                extractor_model="gpt-4o-mini",
            ),
            safety=SafetyBounds(
                quality_threshold=self.config.quality_threshold,
            ),
            evaluation=EvalConfig(
                initial_threshold=self.config.quality_threshold,
            ),
        )

        nathan_config.ensure_directories()

        self._store = MemoryStore(nathan_config)
        self._llm = LearningLLM(nathan_config)

        # Capture initial memory snapshot
        self.metrics.snapshot_memory(self.memories_dir)

        logger.info("LearningLLM initialized for namespace '%s'", self.namespace)

    def run_scenario(
        self,
        tasks: list[str],
        max_calls: int | None = None,
    ) -> ValidationResult:
        """Execute validation scenario.

        Args:
            tasks: List of task strings to execute.
            max_calls: Optional max number of calls (overrides len(tasks)).

        Returns:
            ValidationResult with success status and metrics.
        """
        if self._llm is None:
            self.setup()

        if max_calls is not None:
            tasks = tasks[:max_calls]

        logger.info("Starting validation with %d tasks", len(tasks))

        call_results = []

        for i, task in enumerate(tasks):
            # Check cost budget before call
            current_cost = self.metrics._estimate_cost()
            if current_cost >= self.config.max_cost_usd:
                error_msg = f"Cost budget exceeded: ${current_cost:.2f} >= ${self.config.max_cost_usd:.2f}"
                logger.error(error_msg)
                return ValidationResult(
                    success=False,
                    total_calls=i,
                    total_tokens=self.metrics.total_tokens,
                    estimated_cost_usd=current_cost,
                    metrics=self.metrics.export(),
                    error=error_msg,
                )

            # Execute LLM call
            try:
                start_time = time.time()
                result = self._llm.call(task)
                duration = time.time() - start_time

                # Record metrics
                self.metrics.record_call(
                    duration_s=duration,
                    quality_score=result.score,
                    tokens_used=getattr(result, "tokens_used", 0),  # If available
                )

                # Save call log
                call_data = {
                    "task": task,
                    "response": result.response[:200],  # Truncate for artifacts
                    "quality_score": result.score,
                    "duration_s": duration,
                    "success": True,
                }
                self.artifacts.save_log(i, call_data)

                call_results.append(call_data)

                logger.info(
                    "Call %d/%d: score=%.3f, duration=%.2fs",
                    i + 1,
                    len(tasks),
                    result.score,
                    duration,
                )

            except Exception as e:
                logger.error("Call %d failed: %s", i, e)
                call_data = {
                    "task": task,
                    "error": str(e),
                    "success": False,
                }
                call_results.append(call_data)
                self.artifacts.save_log(i, call_data)

        # Capture final memory snapshot
        final_snapshot = self.metrics.snapshot_memory(self.memories_dir)
        self.artifacts.save_snapshot("final", final_snapshot)

        # Export metrics
        metrics_export = self.metrics.export()
        self.artifacts.save_metrics(metrics_export)

        # Generate report
        report = self.artifacts.generate_report(metrics_export)
        logger.info("\n%s", report)

        return ValidationResult(
            success=True,
            total_calls=len(tasks),
            total_tokens=self.metrics.total_tokens,
            estimated_cost_usd=self.metrics._estimate_cost(),
            metrics=metrics_export,
        )

    def cleanup(self) -> None:
        """Cleanup resources.

        Closes LLM connections and optionally cleans up memory directory.
        """
        if self.config.cleanup_memories and self.memories_dir.exists():
            import shutil

            shutil.rmtree(self.memories_dir)
            logger.info("Cleaned up memory directory: %s", self.memories_dir)

        self._llm = None
        self._store = None
