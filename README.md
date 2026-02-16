# netanel-core-validation

**Production-grade validation suite for netanel-core library.**

Real-world validation with NASA-grade standards before PyPI publication.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What This Is

Comprehensive validation framework that proves **netanel-core** works in production scenarios with real LLM calls.

**Purpose:** Validate learning algorithm, memory persistence, and prompt evolution before publishing to PyPI.

**Not:** Unit tests (netanel-core has 354 of those). This is end-to-end production validation.

---

## Features

✅ **4 Test Scenarios** - Basic learning, evolution, stress test, edge cases  
✅ **Real LLM Calls** - No mocks, uses actual OpenAI API  
✅ **NASA-Grade Standards** - No compromises on quality  
✅ **Cost-Bounded** - ~$0.65 total budget, monitored automatically  
✅ **Complete Metrics** - Latency, quality, memory, cost tracking  
✅ **Rich Artifacts** - Logs, snapshots, reports for inspection  

---

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key
- netanel-core library (local or from PyPI)

### Installation

```bash
# Clone repository
git clone https://github.com/netanel-systems/netanel-core-validation.git
cd netanel-core-validation

# Install dependencies
pip install -e .

# Set API key
export OPENAI_API_KEY="your-api-key-here"
```

### Run All Scenarios

```bash
pytest validation/scenarios/
```

### Run Individual Scenarios

```bash
# Scenario 1: Basic Learning (10 calls, ~$0.05)
pytest validation/scenarios/test_basic_learning.py -v

# Scenario 2: Full Loop + Evolution (40 calls, ~$0.15)
pytest validation/scenarios/test_full_loop.py -v

# Scenario 3: Stress Test (50 calls, ~$0.25)
pytest validation/scenarios/test_stress.py -v

# Scenario 4: Edge Cases (10 calls, ~$0.10)
pytest validation/scenarios/test_edge_cases.py -v
```

---

## Test Scenarios

### Scenario 1: Basic Learning Loop

**What:** 10 real LLM calls testing core learning pipeline  
**Budget:** ~$0.05  
**Validates:** Quality scores, memory persistence, learning extraction

**Success Criteria:**
- All 10 calls complete successfully
- Quality scores >= 0.7
- Memory persists (patterns stored)
- Learnings extracted from responses

**Run:**
```bash
pytest -m scenario1 -v
```

### Scenario 2: Full Loop with Evolution

**What:** 30 calls to trigger evolution + session restart  
**Budget:** ~$0.15  
**Validates:** Prompt evolution, memory survives restart

**Success Criteria:**
- Evolution triggers after ~10-15 calls
- Prompt updated in memory
- Memory survives session restart
- Evolved prompt used in resumed session

**Run:**
```bash
pytest -m scenario2 -v
```

### Scenario 3: Stress Test

**What:** 50 calls validating high-volume handling  
**Budget:** ~$0.25  
**Validates:** No crashes, quality maintained, cost controlled

**Success Criteria:**
- All 50 calls complete without crashes
- Quality scores >= 0.7
- Cost within budget ($1.00 max)

**Run:**
```bash
pytest -m scenario3 -v
```

### Scenario 4: Edge Cases

**What:** 10 edge case tasks (short, long, special chars, duplicates)  
**Budget:** ~$0.10  
**Validates:** Robust handling of unusual inputs

**Success Criteria:**
- All calls complete without crashes
- Quality >= 0.5 (lower for edge cases)

**Run:**
```bash
pytest -m scenario4 -v
```

---

## Configuration

Create `.env` file to override defaults:

```env
# Quality thresholds
VALIDATION_QUALITY_THRESHOLD=0.7

# Cost limits
VALIDATION_MAX_COST_USD=1.00

# Timeouts
VALIDATION_TIMEOUT_SECONDS=30

# Retry policy
VALIDATION_MAX_RETRIES=3
VALIDATION_RETRY_DELAY_SECONDS=5

# Cleanup
VALIDATION_CLEANUP_MEMORIES=true
VALIDATION_SAVE_ARTIFACTS=true
VALIDATION_ARTIFACTS_DIR=artifacts
```

Or configure via environment variables:

```bash
export VALIDATION_QUALITY_THRESHOLD=0.8
export VALIDATION_MAX_COST_USD=2.00
pytest validation/scenarios/
```

---

## Artifacts

After running validation, inspect artifacts:

```
artifacts/
├── calls.jsonl           # Full LLM call history
├── metrics.json          # Performance metrics
├── report.md             # Human-readable summary
└── snapshots/
    ├── initial.json      # Memory state before
    └── final.json        # Memory state after
```

**View report:**
```bash
cat artifacts/report.md
```

**Analyze metrics:**
```bash
cat artifacts/metrics.json | jq .
```

---

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete system design.

**Core Components:**
1. **LearningValidator** - Orchestrates validation runs
2. **MetricsCollector** - Tracks latency, quality, memory, cost
3. **ArtifactManager** - Saves logs, snapshots, reports
4. **Assertions** - Enforces success criteria
5. **ValidationConfig** - Flexible Pydantic settings
6. **Lifecycle** - Pytest fixtures for test isolation

---

## Success Criteria for PyPI

**netanel-core is ready for PyPI when:**

| Metric | Threshold | Status |
|--------|-----------|--------|
| Quality scores | >= 0.7 consistently | ⏳ Pending |
| Memory persistence | 100% across restarts | ⏳ Pending |
| Learnings extracted | > 0 per call | ⏳ Pending |
| Prompt evolution | Triggers correctly | ⏳ Pending |
| Error handling | No crashes | ⏳ Pending |
| Total cost | < $0.65 | ⏳ Pending |

**Run validation to update status:**
```bash
pytest validation/scenarios/ -v
```

---

## Troubleshooting

### "netanel-core not installed"

```bash
# Install from local path
cd ../netanel-core
pip install -e .

# Or wait for PyPI publication
pip install netanel-core
```

### "Rate limit exceeded"

OpenAI has rate limits. Wait 60s or use lower volume:

```bash
# Run just Scenario 1 (10 calls)
pytest -m scenario1
```

### "Cost budget exceeded"

Validation stops automatically at $1.00. Increase if needed:

```bash
export VALIDATION_MAX_COST_USD=2.00
pytest validation/scenarios/
```

### Tests failing?

**This is expected!** Validation reveals bugs. That's the goal.

1. Check `artifacts/report.md` for details
2. Inspect `artifacts/calls.jsonl` for failures
3. Fix netanel-core issues
4. Re-run validation

---

## Development

### Run with coverage

```bash
pytest validation/scenarios/ --cov=validation --cov-report=html
open htmlcov/index.html
```

### Format code

```bash
black validation/
ruff check validation/ --fix
```

### Add new tasks

Edit `validation/tasks/code_generation.py`:

```python
CODING_TASKS = [
    # ... existing tasks
    "Your new coding task here.",
]
```

---

## Contributing

This is a Netanel Systems internal project. PRs welcome from team members.

**Process:**
1. Follow [Twelve Gates](TWELVE_GATES_V4.md) process
2. Get CodeRabbit approval
3. All scenarios must pass
4. Cost within budget

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Links

- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **netanel-core:** [github.com/netanel-systems/netanel-core](https://github.com/netanel-systems/netanel-core)
- **Company:** [www.netanel.systems](https://www.netanel.systems)

---

*Part of Netanel Systems - "Gift of God" (Hebrew: נתנאל)*

*Building NASA-grade agentic systems with no compromises.*
