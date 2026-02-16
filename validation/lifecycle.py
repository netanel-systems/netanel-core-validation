"""Pytest fixtures for test lifecycle management.

Provides setup/teardown for validation scenarios:
- Temporary memory directories (isolated per scenario)
- Artifact directories
- Cleanup between scenarios
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Generator

import pytest

from validation.config import ValidationConfig


@pytest.fixture
def config() -> ValidationConfig:
    """Provide default validation configuration.

    Can be overridden in tests by passing custom ValidationConfig.
    """
    return ValidationConfig()


@pytest.fixture
def memories_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Provide isolated temporary memory directory for each scenario.

    Automatically cleans up after test completes.

    Args:
        tmp_path: Pytest's built-in tmp_path fixture.

    Yields:
        Path to temporary memory directory.
    """
    memory_path = tmp_path / "memories"
    memory_path.mkdir(parents=True, exist_ok=True)

    yield memory_path

    # Cleanup after test
    if memory_path.exists():
        shutil.rmtree(memory_path)


@pytest.fixture
def artifacts_dir(tmp_path: Path, config: ValidationConfig) -> Generator[Path, None, None]:
    """Provide artifacts directory for saving validation outputs.

    If config.save_artifacts is False, returns None and no directory is created.

    Args:
        tmp_path: Pytest's built-in tmp_path fixture.
        config: Validation configuration.

    Yields:
        Path to artifacts directory or None if artifacts disabled.
    """
    if not config.save_artifacts:
        yield None
        return

    artifacts_path = tmp_path / config.artifacts_dir
    artifacts_path.mkdir(parents=True, exist_ok=True)

    yield artifacts_path

    # Artifacts are kept for inspection (not cleaned up automatically)


@pytest.fixture(autouse=True)
def isolate_scenarios() -> Generator[None, None, None]:
    """Ensure complete isolation between scenario runs.

    This fixture runs automatically for all tests.
    Prevents state leakage between scenarios.
    """
    # Setup: nothing needed (isolation via separate memory dirs)
    yield
    # Teardown: pytest tmp_path cleanup handles it
