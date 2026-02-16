# Implementation Plan - Validation Framework

**Gate 3: Our Plan**
**Dependencies:** Gate 2 (Scope) must be unconditionally approved

---

## Implementation Order

### Phase 1: Foundation (Infrastructure)
**Priority:** CRITICAL - Everything depends on this

1. **pyproject.toml** - Project setup
   - Dependencies: pytest, netanel-core (local path), openai
   - Project metadata
   - Build configuration

2. **pytest.ini** - Test configuration
   - Test discovery patterns
   - Logging configuration
   - Markers for scenarios

3. **.gitignore** - Ignore generated files
   - memories/
   - artifacts/
   - __pycache__/
   - .pytest_cache/

4. **validation/__init__.py** - Package initialization
   - Version info
   - Public API exports

### Phase 2: Configuration (Enables Flexibility)
**Priority:** HIGH - Needed by all components

5. **validation/config.py** - Pydantic settings
   ```python
   class ValidationConfig(BaseSettings):
       quality_threshold: float = 0.7
       max_cost_usd: float = 1.00
       timeout_seconds: int = 30
       max_retries: int = 3
       retry_delay_seconds: int = 5
   ```

### Phase 3: Core Components (Building Blocks)
**Priority:** HIGH - Foundation for scenarios

6. **validation/lifecycle.py** - Setup/teardown fixtures
   - pytest fixtures for temp directories
   - Memory cleanup between scenarios
   - Artifact directory setup

7. **validation/metrics.py** - MetricsCollector
   - Track latency (start/end timestamps)
   - Track quality scores
   - Track memory growth (file counts, sizes)
   - Track cost (tokens, API calls)
   - Export to JSON

8. **validation/artifacts.py** - ArtifactManager
   - Save logs (LLM calls, responses)
   - Capture memory snapshots
   - Generate reports (markdown, JSON)
   - Archive artifacts by timestamp

9. **validation/assertions.py** - Validation assertions
   - assert_quality_threshold(scores, min_threshold)
   - assert_memory_persisted(before, after)
   - assert_no_crashes(results)
   - assert_learning_extracted(memory_snapshot)

10. **validation/validator.py** - LearningValidator orchestrator
    - Initialize LearningLLM from netanel-core
    - Execute tasks sequentially
    - Collect metrics per call
    - Enforce config bounds (cost, timeout)
    - Return ValidationResult

### Phase 4: Task Datasets (Test Data)
**Priority:** MEDIUM - Needed before scenarios

11. **validation/tasks/__init__.py** - Package init
12. **validation/tasks/code_generation.py** - Task datasets
    - 50+ diverse coding tasks
    - Varying complexity (easy, medium, hard)
    - Different domains (web, data, algorithms)

### Phase 5: Test Scenarios (The Validation)
**Priority:** HIGH - Core deliverable

13. **validation/scenarios/__init__.py** - Package init

14. **validation/scenarios/test_basic_learning.py** - Scenario 1
    - 10 LLM calls
    - Verify quality, memory, learnings
    - ~$0.05 budget

15. **validation/scenarios/test_full_loop.py** - Scenario 2
    - 30 LLM calls to trigger evolution
    - Restart session (new LearningLLM, same memories_dir)
    - Verify evolution + restart
    - ~$0.15 budget

16. **validation/scenarios/test_stress.py** - Scenario 3
    - 50 LLM calls with error injection
    - Verify retries, recovery
    - ~$0.25 budget

17. **validation/scenarios/test_edge_cases.py** - Scenario 4
    - Network timeouts (mock)
    - Rate limiting (mock 429)
    - Malformed responses
    - Corrupted memory recovery
    - ~$0.10 budget

### Phase 6: Documentation
**Priority:** HIGH - Required for PyPI

18. **ARCHITECTURE.md** - Complete architecture doc
    - System design
    - Component details
    - Success criteria
    - Design decisions

19. **README.md** - Usage guide
    - Setup instructions
    - Running validation
    - Interpreting results
    - Contributing guidelines

### Phase 7: CI/CD
**Priority:** MEDIUM - Automation

20. **.github/workflows/validate.yml** - GitHub Actions
    - Trigger on PR
    - Setup Python 3.12
    - Install dependencies
    - Run pytest
    - Upload artifacts
    - Fail if cost > $1.00

---

## Development Workflow

### Step-by-Step Execution

**Day 1: Foundation + Core (Items 1-10)**
- Morning: Infrastructure (1-4)
- Afternoon: Config + Lifecycle (5-6)
- Evening: Metrics + Artifacts + Assertions (7-9)
- Night: Validator orchestrator (10)

**Day 2: Scenarios + Docs (Items 11-20)**
- Morning: Task datasets (11-12)
- Afternoon: Scenarios 1-2 (13-15)
- Evening: Scenarios 3-4 (16-17)
- Night: Documentation + CI/CD (18-20)

### Testing Strategy

**Per Component:**
- Unit tests for each module
- Test coverage >= 80%
- All edge cases covered

**Integration:**
- Run Scenario 1 first (basic)
- If passes → Run Scenarios 2-4
- If fails → Fix netanel-core or validation code

### Quality Gates

**Before PR:**
- ✅ All unit tests pass
- ✅ All 4 scenarios pass with real LLM calls
- ✅ Total cost < $0.65
- ✅ No pytest warnings
- ✅ Documentation complete

---

## Risk Management

### Risk 1: API Costs Exceed Budget
- **Mitigation:** Stop on $1.00 limit (enforced in config)
- **Contingency:** Use smaller task datasets if needed

### Risk 2: netanel-core Has Bugs
- **Mitigation:** This is the GOAL - find bugs before PyPI
- **Contingency:** Document issues, fix in netanel-core, re-validate

### Risk 3: Scenarios Take Too Long
- **Mitigation:** Timeouts per call (30s default)
- **Contingency:** Reduce task count if needed

### Risk 4: Memory/Disk Issues
- **Mitigation:** Cleanup between scenarios
- **Contingency:** Smaller memory limits, artifact cleanup

---

## Success Metrics

### Code Metrics
- Lines of code: ~2,000-3,000 (estimated)
- Test coverage: >= 80%
- Cyclomatic complexity: < 10 per function

### Validation Metrics
- All 4 scenarios pass: ✅
- Quality scores: >= 0.7 (avg)
- Memory persistence: 100%
- Evolution triggers: Yes
- Error handling: Robust
- Cost: < $0.65

### Time Metrics
- Development: 24 hours
- PR review + fixes: 12 hours
- Total: 36 hours (1.5 days)

---

## Dependencies

### External
- netanel-core (local path: `../netanel-core`)
- pytest >= 8.0
- openai >= 1.0
- pydantic-settings >= 2.0

### Internal
- None (fresh project)

---

## Acceptance Criteria

**This plan is ready when:**
- ✅ CodeRabbit approves this plan (Gate 4)
- ✅ Comparison with CodeRabbit's plan complete (Gate 5)
- ✅ Final plan agreed upon (Gate 6)
- ✅ Ready to start building (Gate 7)

---

**Status:** DRAFT - Awaiting Gate 2 approval before submitting
