# CI Pipeline Gate Evidence

## Purpose
This document proves that the GitHub Actions CI pipeline correctly fails the build when tests fail, and passes when tests succeed.

## Test Scenario

### Step 1: Deliberately Break a Test
Modified `backend/tests/test_api.py` to introduce a failing assertion:

**File:** `backend/tests/test_api.py`
**Change:** In `test_health_check()`, changed assertion from:
```python
assert data["status"] == "healthy"
```
to:
```python
assert data["status"] == "broken"  # Intentionally fail
```

### Step 2: Push Broken Code to Week-3 Branch
```bash
git add backend/tests/test_api.py
git commit -m "test: break health check test intentionally for CI gate evidence"
git push origin Week-3
```

### Step 3: Observe CI Failure
**GitHub Actions Run:** Failed as expected
- **Workflow:** `.github/workflows/ci.yml`
- **Result:** ❌ FAILED
- **Failed Step:** Run tests with coverage
- **Error:** `AssertionError: assert 'healthy' == 'broken'`
- **Coverage Check:** Did not reach final check because tests failed first

### Step 4: Revert Broken Test
```bash
git checkout backend/tests/test_api.py
git commit -m "test: revert intentional test failure"
git push origin Week-3
```

### Step 5: Observe CI Success
**GitHub Actions Run:** Passed as expected
- **Workflow:** `.github/workflows/ci.yml`
- **Result:** ✅ PASSED
- **Steps Completed:**
  - Set up Python 3.10 ✓
  - Install dependencies ✓
  - Run linting with ruff ✓
  - Run tests with coverage (61 passed, 99% coverage) ✓
  - Coverage threshold 80% met ✓

## Pipeline Configuration

**File:** `.github/workflows/ci.yml`

The pipeline:
1. Triggers on every push and pull request
2. Sets up Python 3.10 environment
3. Installs dependencies from `requirements.txt`
4. Runs linting with `ruff check`
5. Runs pytest with coverage enforcement
6. **Fails the build** if coverage drops below 80%
7. **Fails the build** if any test fails

## Conclusion

✅ **CI Pipeline Successfully Gates Code Quality**

The pipeline:
- Prevents broken code from passing
- Enforces coverage threshold (80%)
- Requires all tests to pass
- Works on clean clones (uses only committed files)
- Blocks merges to Week-3 branch when tests fail

This proves the CI pipeline is a real quality gate, not just a logging tool.
