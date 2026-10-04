# Refactor: Extract Duplicate Collection Validation

## Code Smell
**Duplication** — The collection validation logic appeared identically in two endpoint handlers: `create_prompt()` and `update_prompt()`. Both performed the same check:
```python
if prompt_data.collection_id:
    collection = storage.get_collection(prompt_data.collection_id)
    if not collection:
        raise HTTPException(status_code=400, detail="Collection not found")
```

This violates the DRY (Don't Repeat Yourself) principle and makes maintenance harder if the validation rules change.

## Before Refactor
**Commit:** `8a361c9`

The validation code was duplicated across two functions in `backend/app/api.py`.

## After Refactor
**Commit:** `ead3e69`

Created a helper function `validate_collection_exists(collection_id: Optional[str])` that:
- Takes an optional collection ID
- Raises `HTTPException(400, "Collection not found")` if the ID is provided but doesn't exist
- Returns normally (None) if validation passes

Both `create_prompt()` and `update_prompt()` now call this helper instead of duplicating the logic.

## Verification

### Tests Pass Before and After
- **Before:** 61 tests passed, 99% coverage
- **After:** 61 tests passed, 99% coverage

All tests in `tests/test_api.py`, `tests/test_storage.py`, and `tests/test_utils.py` continue to pass, including:
- `test_create_prompt_invalid_collection` — validates 400 error for invalid collection
- `test_update_prompt_invalid_collection` — validates 400 error for invalid collection

### Public Interface Unchanged
- Both endpoints still accept the same request shapes
- Both endpoints return the same response shapes
- Both endpoints raise `HTTPException(400)` for invalid collections
- No changes to request/response models

### Observable Behavior Unchanged
- Error messages remain identical
- HTTP status codes remain identical
- Successful creation and updates work exactly as before
- Collection validation occurs at the same point in the request lifecycle

## Code Quality Impact
- **Lines of code:** Reduced duplication
- **Maintainability:** Single source of truth for collection validation
- **Testability:** Validation logic tested through existing endpoint tests
- **No behavior changes:** All existing tests pass without modification
