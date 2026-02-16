# Validation Framework Architecture

**Version:** 1.0  
**Status:** Implemented  
**Stakeholders:** Nathan + CodeRabbit

---

## Executive Summary

Production-grade validation framework for **netanel-core** library before PyPI publication.

**Purpose:** Prove netanel-core works in real-world scenarios with NASA-grade quality standards.

**Scope:** 6 core components, 4 test scenarios, ~$0.65 budget, 24-hour implementation.

**Outcome:** Confidence to publish netanel-core to PyPI or identification of issues to fix.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Validation Framework                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐         ┌──────────────────┐           │
│  │ LearningValidator│◄────────│  Test Scenarios  │           │
│  │  (Orchestrator)  │         │  - Basic Learning│           │
│  └────────┬─────────┘         │  - Full Loop     │           │
│           │                   │  - Stress Test   │           │
│           │                   │  - Edge Cases    │           │
│           │                   └──────────────────┘           │
│           │                                                  │
│           ├──────►┌──────────────────┐                      │
│           │       │ValidationConfig  │                      │
│           │       │(Pydantic Settings)│                      │
│           │       └──────────────────┘                      │
│           │                                                  │
│           ├──────►┌──────────────────┐                      │
│           │       │ MetricsCollector │                      │
│           │       │ - Latency        │                      │
│           │       │ - Quality        │                      │
│           │       │ - Memory growth  │                      │
│           │       │ - Cost           │                      │
│           │       └──────────────────┘                      │
│           │                                                  │
│           ├──────►┌──────────────────┐                      │
│           │       │ ArtifactManager  │                      │
│           │       │ - Logs           │                      │
│           │       │ - Snapshots      │                      │
│           │       │ - Reports        │                      │
│           │       └──────────────────┘                      │
│           │                                                  │
│           └──────►┌──────────────────┐                      │
│                   │ Assertions       │                      │
│                   │ - Quality bounds │                      │
│                   │ - Memory checks  │                      │
│                   │ - No crashes     │                      │
│                   └──────────────────┘                      │
│                                                              │
│           Uses ▼                                             │
│  ┌────────────────────────┐                                 │
│  │   netanel-core         │                                 │
│  │   (LearningLLM)        │                                 │
│  └────────────────────────┘                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. ValidationConfig (config.py)

**Purpose:** Flexible configuration for validation parameters.

**Key Settings:**
- `quality_threshold` (0.7) - Minimum acceptable LLM quality
- `max_cost_usd` (1.00) - Budget limit
- `timeout_seconds` (30) - Call timeout
- `max_retries` (3) - Retry policy
- `cleanup_memories` (True) - Auto-cleanup

**Why:** Enables tuning without code changes, essential for different environments.

### 2. LearningValidator (validator.py)

**Purpose:** Orchestrate validation runs end-to-end.

**Key Methods:**
- `setup()` - Initialize LearningLLM
- `run_scenario(tasks, max_calls)` - Execute validation
- `cleanup()` - Clean up resources

**Flow:**
1. Setup netanel-core LearningLLM
2. Capture initial memory snapshot
3. Execute tasks sequentially
4. Collect metrics per call
5. Enforce cost/timeout bounds
6. Generate artifacts
7. Return ValidationResult

### 3. MetricsCollector (metrics.py)

**Purpose:** Track performance and quality metrics.

**Metrics:**
- **Latency:** min, max, mean, p50, p95, p99
- **Quality:** min, max, mean, std dev
- **Memory:** files created, size growth, patterns, evolutions
- **Cost:** tokens used, estimated USD

**Why:** Measurable validation of success criteria.

### 4. ArtifactManager (artifacts.py)

**Purpose:** Save validation outputs for inspection.

**Artifacts:**
- `calls.jsonl` - Full LLM call history
- `snapshots/*.json` - Memory state snapshots
- `metrics.json` - Exported metrics
- `report.md` - Human-readable summary

**Why:** Critical for debugging failures and analyzing results.

### 5. Assertions (assertions.py)

**Purpose:** Enforce quality bounds.

**Functions:**
- `assert_quality_threshold(scores, min)` - All scores >= threshold
- `assert_memory_persisted(before, after)` - Memory grew
- `assert_no_crashes(results)` - All calls succeeded
- `assert_learning_extracted(snapshot)` - Learnings stored
- `assert_evolution_triggered(before, after)` - Evolution occurred
- `assert_cost_within_budget(actual, max)` - Cost controlled

**Why:** Clear pass/fail criteria for validation.

### 6. Lifecycle (lifecycle.py)

**Purpose:** Pytest fixtures for test isolation.

**Fixtures:**
- `config()` - ValidationConfig instance
- `memories_dir(tmp_path)` - Isolated temp directory per scenario
- `artifacts_dir(tmp_path)` - Artifacts output directory
- `isolate_scenarios()` - Autouse fixture for complete isolation

**Why:** Prevents test pollution, ensures reproducibility.

---

## Test Scenarios

### Scenario 1: Basic Learning Loop

**File:** `test_basic_learning.py`  
**Budget:** ~$0.05  
**Tasks:** 10 coding tasks

**Tests:**
- Core learning pipeline works
- Quality scores >= 0.7
- Memory persists (patterns stored)
- Learnings extracted

**Success Criteria:**
- ✅ All 10 calls complete
- ✅ Quality >= 0.7
- ✅ Memory growth > 0
- ✅ Patterns stored >= 1

### Scenario 2: Full Loop with Evolution

**File:** `test_full_loop.py`  
**Budget:** ~$0.15  
**Tasks:** 30 calls + 10 restart calls

**Tests:**
- Prompt evolution triggers (~10-15 calls)
- Memory survives session restart
- Evolved prompt used in resumed session

**Success Criteria:**
- ✅ Evolution triggered
- ✅ Memory persists across restart
- ✅ Quality maintained with evolved prompt

### Scenario 3: Stress Test

**File:** `test_stress.py`  
**Budget:** ~$0.25  
**Tasks:** 50 coding tasks

**Tests:**
- High volume handling
- No crashes under load
- Quality maintained
- Cost within budget

**Success Criteria:**
- ✅ All 50 calls complete
- ✅ No crashes
- ✅ Quality >= 0.7
- ✅ Cost < $1.00

### Scenario 4: Edge Cases

**File:** `test_edge_cases.py`  
**Budget:** ~$0.10  
**Tasks:** 10 edge case tasks

**Tests:**
- Very short tasks
- Very long tasks
- Special characters (UTF-8, emojis)
- Repeated/duplicate tasks

**Success Criteria:**
- ✅ All calls complete without crashes
- ✅ Quality >= 0.5 (lower for edge cases)

---

## Success Criteria for PyPI Publication

All scenarios must pass with these thresholds:

| Metric | Threshold | Why |
|--------|-----------|-----|
| Quality scores | >= 0.7 consistently | Ensures useful responses |
| Memory persistence | 100% across restarts | Critical for learning |
| Learnings extracted | > 0 per call | Confirms learning works |
| Prompt evolution | Triggers correctly | Core feature validation |
| Error handling | No crashes | Production robustness |
| Total cost | < $0.65 | Affordable for validation |

**If ANY scenario fails:** Investigation required, fix netanel-core if needed, re-validate.

---

## Implementation Status

| Component | Status | Lines | Tests |
|-----------|--------|-------|-------|
| config.py | ✅ Complete | ~60 | Validated by usage |
| validator.py | ✅ Complete | ~140 | Integration tests |
| metrics.py | ✅ Complete | ~120 | Scenario tests |
| artifacts.py | ✅ Complete | ~80 | Scenario tests |
| assertions.py | ✅ Complete | ~70 | Scenario tests |
| lifecycle.py | ✅ Complete | ~50 | Pytest fixtures |
| test_basic_learning.py | ✅ Complete | ~40 | Scenario 1 |
| test_full_loop.py | ✅ Complete | ~50 | Scenario 2 |
| test_stress.py | ✅ Complete | ~35 | Scenario 3 |
| test_edge_cases.py | ✅ Complete | ~40 | Scenario 4 |
| code_generation.py | ✅ Complete | ~60 | 55 tasks |

**Total:** ~745 lines of code, 4 complete scenarios, all components implemented.

---

## Design Decisions

### Why Real LLM Calls, Not Mocks?

**Decision:** Use real OpenAI API calls for all validation.

**Reasoning:**
- Mocks don't test real behavior (API latency, errors, token limits)
- Production validation requires production conditions
- Cost is acceptable ($0.65 total)

**Trade-off:** Tests require API key and cost money, but provide real confidence.

### Why gpt-4o-mini?

**Decision:** Use gpt-4o-mini for all LLM calls.

**Reasoning:**
- Cheapest model ($0.15/1M input, $0.60/1M output)
- Still high quality for coding tasks
- netanel-core should work with any model

**Trade-off:** Doesn't test with more expensive models, but validates core logic.

### Why Separate Scenarios Instead of One Big Test?

**Decision:** 4 separate pytest tests, one per scenario.

**Reasoning:**
- Clear isolation (each scenario has own memory dir)
- Easier to debug failures (know which scenario failed)
- Can run individually (pytest -k scenario1)
- Better reporting

**Trade-off:** Slightly more boilerplate, but worth it for clarity.

### Why Defer Regression Tracking?

**Decision:** No baseline/regression tracking in initial validation.

**Reasoning:**
- This is pre-PyPI validation (prove it works ONCE)
- Regression tracking is for ongoing monitoring (post-PyPI)
- Would add complexity without value for initial validation

**Post-PyPI:** Add regression tracking in v2.0 for continuous monitoring.

---

## Dependencies

```toml
[project.dependencies]
pytest = ">=8.0.0"
pytest-asyncio = ">=0.23.0"
openai = ">=1.0.0"
pydantic = ">=2.0.0"
pydantic-settings = ">=2.0.0"
```

**Local dependency:** netanel-core (from `../netanel-core`)

**Why local:** Validating pre-publication, need immediate access to changes.

**After PyPI:** Update to `netanel-core = "^0.1.0"` once published.

---

## CI/CD Integration

**Not implemented yet.** Documented approach:

**GitHub Actions Workflow:**
```yaml
name: Validate netanel-core

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -e .
      - run: pytest validation/scenarios/
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      - uses: actions/upload-artifact@v4
        with:
          name: validation-artifacts
          path: artifacts/
```

**Future enhancement:** Add cost monitoring, fail if > $1.00.

---

## Non-Functional Requirements

### Performance
- Each scenario completes in < 5 minutes
- Total suite run < 15 minutes
- Minimal memory footprint (< 500MB)

### Cost
- Full suite run < $0.65
- Individual scenario < $0.25
- Affordable for frequent runs

### Reliability
- Zero tolerance for crashes
- Graceful error handling
- Clear failure messages

### Observability
- Full logs of all LLM interactions
- Metrics exported for analysis
- Human-readable reports generated

---

## Future Enhancements (Post-PyPI v2.0)

Not in scope for initial validation:

1. **Baseline & Regression Tracking** - Track performance over time
2. **Concurrency Testing** - Test parallel LLM calls
3. **Version Matrix Testing** - Python 3.10, 3.11, 3.12
4. **Model Comparison** - Validate with Claude, GPT-4, etc.
5. **Performance Benchmarks** - Track speed improvements

---

## Lessons Learned

1. **CodeRabbit feedback improved architecture significantly** - Added config layer, lifecycle, edge cases
2. **Defer wisely** - Regression tracking is valuable but wrong scope for initial validation
3. **Real tests > mocks** - Worth the cost for confidence
4. **Clear success criteria** - 9 specific checkpoints leave no ambiguity

---

**Last Updated:** 2026-02-16  
**Review Status:** Implementation complete, ready for testing
