# Validation Framework Architecture

**Version:** 1.0
**Status:** Gate 1 Review
**Stakeholders:** Nathan + CodeRabbit

---

## Purpose

Production-grade validation framework for **netanel-core** library before PyPI publication.

**Goals:**
- Validate learning algorithm works in real-world scenarios
- Test memory persistence across sessions
- Verify prompt evolution triggers correctly
- Stress test error handling and retries
- Prove production-readiness with NASA-grade standards

**Non-Goals:**
- Unit tests (already covered by netanel-core's 354 tests)
- Mocked validation (all tests use real LLM API calls)
- Feature development (pure validation only)

---

## Architecture Overview

### System Diagram

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
│           │                   └──────────────────┘           │
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
│           ▼ Uses                                             │
│  ┌────────────────────────┐                                 │
│  │   netanel-core         │                                 │
│  │   (LearningLLM)        │                                 │
│  └────────────────────────┘                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
netanel-core-validation/
├── validation/
│   ├── __init__.py
│   ├── validator.py         # LearningValidator orchestrator
│   ├── metrics.py            # MetricsCollector
│   ├── artifacts.py          # ArtifactManager
│   ├── assertions.py         # Validation assertions
│   ├── scenarios/
│   │   ├── __init__.py
│   │   ├── test_basic_learning.py      # Scenario 1
│   │   ├── test_full_loop.py           # Scenario 2
│   │   └── test_stress.py              # Scenario 3
│   └── tasks/
│       ├── __init__.py
│       └── code_generation.py          # Task datasets
├── memories/                 # netanel-core memory (gitignored)
├── artifacts/                # Test outputs (gitignored)
├── pyproject.toml
├── pytest.ini
├── .gitignore
├── ARCHITECTURE.md           # This file
├── TWELVE_GATES_V4.md
└── README.md
```

---

## Core Components

### 1. LearningValidator (validator.py)

**Responsibility:** Orchestrate validation runs end-to-end.

**Interface:**
```python
class LearningValidator:
    def __init__(
        self,
        namespace: str,
        memories_dir: Path,
        artifacts_dir: Path,
    ) -> None: ...

    def run_scenario(
        self,
        tasks: list[str],
        max_calls: int,
    ) -> ValidationResult: ...

    def cleanup(self) -> None: ...
```

**Key Methods:**
- `run_scenario()` - Execute N LLM calls, collect metrics, verify assertions
- `cleanup()` - Clean up temp files, close resources

### 2. MetricsCollector (metrics.py)

**Responsibility:** Track performance and quality metrics.

**Metrics Tracked:**
- **Latency:** Time per LLM call (p50, p95, p99)
- **Quality:** Score distribution (min, max, avg, std dev)
- **Memory Growth:** Files created, patterns stored, evolutions triggered
- **Cost:** API usage (tokens, dollars)

**Interface:**
```python
class MetricsCollector:
    def record_call(
        self,
        duration_s: float,
        quality_score: float,
        tokens_used: int,
    ) -> None: ...

    def snapshot_memory(self, memories_dir: Path) -> MemorySnapshot: ...

    def export(self) -> dict[str, Any]: ...
```

### 3. ArtifactManager (artifacts.py)

**Responsibility:** Save validation outputs for inspection.

**Artifacts Saved:**
- **Logs:** Full LLM call history (task, response, score)
- **Memory Snapshots:** Before/after validation (patterns, evolutions)
- **Metrics:** JSON export of all metrics
- **Reports:** Human-readable summary

**Interface:**
```python
class ArtifactManager:
    def save_log(self, call_index: int, call_data: dict) -> None: ...

    def save_snapshot(self, name: str, snapshot: MemorySnapshot) -> None: ...

    def save_metrics(self, metrics: dict) -> None: ...

    def generate_report(self) -> str: ...
```

### 4. Validation Assertions (assertions.py)

**Responsibility:** Enforce quality bounds.

**Assertions:**
- `assert_quality_threshold(scores, min_threshold=0.7)` - All scores >= 0.7
- `assert_memory_persisted(before, after)` - Memory grew (new patterns stored)
- `assert_no_crashes(results)` - All calls completed successfully
- `assert_learning_extracted(memory_snapshot)` - Learnings stored

---

## Test Scenarios

### Scenario 1: Basic Learning Loop (10 calls)

**Purpose:** Verify core learning pipeline works.

**Steps:**
1. Initialize fresh LearningLLM instance
2. Run 10 diverse coding tasks
3. Collect metrics on each call
4. Verify quality, memory persistence, learnings extracted

**Success Criteria:**
- ✅ All 10 calls complete successfully
- ✅ Quality scores >= 0.7
- ✅ Memory persists (patterns stored)
- ✅ Learnings extracted from responses

**Cost:** ~$0.05 (10 calls × gpt-4o-mini)

### Scenario 2: Full Loop with Evolution (30 calls + restart)

**Purpose:** Validate prompt evolution and session restart.

**Steps:**
1. Run 30 LLM calls to trigger evolution
2. Verify evolution triggered (prompt updated)
3. Restart session (new LearningLLM instance, same memories_dir)
4. Verify memory survives restart
5. Run 10 more calls with evolved prompt

**Success Criteria:**
- ✅ Evolution triggered after ~10-15 calls
- ✅ Prompt updated in memory
- ✅ Memory survives session restart
- ✅ Evolved prompt used in resumed session

**Cost:** ~$0.15 (40 calls × gpt-4o-mini)

### Scenario 3: Stress Test (50 calls + error injection)

**Purpose:** Validate error handling and retries.

**Steps:**
1. Run 50 LLM calls
2. Inject errors (timeout, API failure, low quality)
3. Verify retries work
4. Verify system recovers gracefully

**Success Criteria:**
- ✅ Retries succeed after injected errors
- ✅ System doesn't crash on failures
- ✅ Quality maintained despite errors

**Cost:** ~$0.25 (50 calls + retries × gpt-4o-mini)

---

## Success Criteria for PyPI Publication

All scenarios must pass with these thresholds:

| Metric | Threshold | Why |
|--------|-----------|-----|
| Quality scores | >= 0.7 consistently | Ensures useful responses |
| Memory persistence | 100% across restarts | Critical for learning |
| Learnings extracted | > 0 per call | Confirms learning works |
| Prompt evolution | Triggers correctly | Core feature validation |
| Error handling | No crashes, retries work | Production robustness |
| Total cost | < $0.50 per full suite | Affordable for CI/CD |

**If ANY scenario fails:** Investigation required, fix netanel-core if needed, re-validate.

---

## Dependencies

```toml
[project.dependencies]
python = "^3.12"
pytest = "^8.0"
netanel-core = { path = "../netanel-core", develop = true }  # Local development
openai = "^1.0"
```

**Why local netanel-core:**
- We're validating it BEFORE PyPI publication
- Need to test changes immediately without publishing

**After validation passes:**
- Publish netanel-core to PyPI
- Update dependency to `netanel-core = "^0.1.0"`

---

## Design Principles

1. **Real, Not Mocked** - All LLM calls use real OpenAI API (no mocks)
2. **Comprehensive** - Cover all critical paths (learning, memory, evolution, errors)
3. **Reproducible** - Same tasks, same expected behaviors
4. **Bounded** - Max cost ($0.50), max time (5 min per scenario)
5. **NASA-Grade** - No compromises, no "good enough"
6. **Permanent Solution** - No shortcuts, proper architecture only

---

## Non-Functional Requirements

### Performance
- Each scenario completes in < 5 minutes
- Total suite run < 15 minutes
- Minimal memory footprint (< 500MB)

### Cost
- Full suite run < $0.50
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

## Future Enhancements (Post-PyPI)

Not in scope for initial validation, but potential additions:

1. **More Scenarios** - Test other use cases (chat, analysis, etc.)
2. **Model Comparison** - Validate with different LLMs (Claude, GPT-4)
3. **Performance Benchmarks** - Track speed improvements over time
4. **Regression Detection** - Alert on quality degradation
5. **CI/CD Integration** - Auto-run on netanel-core changes

---

## Open Questions for Review

1. **Is this architecture complete?** Any missing components?
2. **Are 3 scenarios sufficient?** What else should we validate?
3. **Success criteria appropriate?** Any gaps in thresholds?
4. **Structure makes sense?** Any improvements to organization?

---

**Review Status:** Awaiting Gate 1 unconditional approval from CodeRabbit.
