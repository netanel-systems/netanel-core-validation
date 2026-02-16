# Validation Framework - Step 1 Implementation Plan

## Scope
Implement validation framework core + Scenario 1 (Basic Learning Loop)

## Checklist

### 1. Project Infrastructure
- [ ] Create pyproject.toml with dependencies (pytest, netanel-core, openai)
- [ ] Create pytest.ini for test configuration
- [ ] Create .gitignore (ignore memories/, __pycache__, .pytest_cache)
- [ ] Set up validation/ directory structure

### 2. Validation Framework Core
- [ ] `validation/__init__.py` - Package initialization
- [ ] `validation/validator.py` - LearningValidator class (orchestrates validation)
- [ ] `validation/metrics.py` - MetricsCollector (track response time, quality, memory growth)
- [ ] `validation/artifacts.py` - ArtifactManager (save results, logs, memory snapshots)
- [ ] `validation/assertions.py` - Validation assertions (quality bounds, memory checks)

### 3. Task Datasets
- [ ] `validation/tasks/__init__.py`
- [ ] `validation/tasks/code_generation.py` - 10+ diverse coding tasks

### 4. Scenario 1: Basic Learning Loop
- [ ] `validation/scenarios/__init__.py`
- [ ] `validation/scenarios/test_basic_learning.py`:
  - 10 real LLM calls through netanel-core
  - Verify: response quality, memory persistence, learning extraction
  - Collect: metrics (latency, cost, quality scores)
  - Generate: artifacts (logs, memory snapshots, metrics.json)

### 5. Documentation
- [ ] ARCHITECTURE.md - Validation framework design
- [ ] Update README.md with usage instructions

## Success Criteria
- ✅ All 10 calls complete successfully
- ✅ Quality scores >= 0.7
- ✅ Memory persists across calls
- ✅ Learnings extracted and stored
- ✅ Metrics collected and saved
- ✅ Zero crashes or hangs

## Cost Estimate
~$0.05 for Scenario 1 (10 calls with gpt-4o-mini)
