# Prompt Versions Specification

## 1. Overview and Goals

Prompt versions add immutable history for each prompt while preserving the existing `Prompt` model and endpoints. A prompt keeps its current ("live") state as today, while a separate version log records snapshots of the prompt state, enabling auditability and rollback via explicit APIs.

Goals:
- Record every prompt state change (create, PUT, PATCH, rollback) as a distinct, immutable version snapshot.
- Allow clients to list versions for a prompt and retrieve a specific version.
- Provide an explicit rollback endpoint that restores a previous version as the new current prompt, without mutating historical versions.

---

## 2. User Stories & Acceptance Criteria

### US1: View prompt version history

As a user, I can see all historical versions of a prompt ordered newest first.

Acceptance criteria:
- Given an existing prompt with one or more versions, `GET /prompts/{id}/versions` returns `200` with a non-empty `versions` array, `total` equal to `len(versions)`, and versions ordered newest-first by `created_at`.
- Given a non-existent prompt ID, `GET /prompts/{id}/versions` returns `404` with `{"detail": "Prompt not found"}`.

### US2: View a specific version

As a user, I can retrieve a specific version of a prompt.

Acceptance criteria:
- Given an existing prompt and version ID, `GET /prompts/{id}/versions/{version_id}` returns `200` with a `PromptVersion` whose `prompt_id` equals the path `id` and `id` equals `version_id`.
- Given an existing prompt but non-existent version ID, the endpoint returns `404` with `{"detail": "Prompt version not found"}`.

### US3: Roll back to a prior version

As a user, I can roll back a prompt to a previous version.

Acceptance criteria:
- Given an existing prompt and valid version ID, `POST /prompts/{id}/versions/{version_id}/rollback` returns `200` with a `Prompt` whose `id` and `created_at` match the original prompt, whose `title`, `content`, `description`, and `collection_id` match the version, and whose `updated_at` is strictly greater than the version’s `created_at`.
- A new version row is created representing the rolled-back state (increasing total version count by 1 for that prompt).
- Given a non-existent prompt ID, the rollback endpoint returns `404` with `{"detail": "Prompt not found"}`.
- Given a non-existent version ID for an existing prompt, the rollback endpoint returns `404` with `{"detail": "Prompt version not found"}`.

---

## 3. Required Data Model Changes

All models extend existing Pydantic & storage patterns.

### 3.1 New Models

```python
class PromptVersionBase(BaseModel):
    prompt_id: str
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None

class PromptVersion(PromptVersionBase):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    version_number: int

class PromptVersionList(BaseModel):
    versions: List[PromptVersion]
    total: int
```

Version semantics:
- A **version** is an immutable snapshot of a prompt’s user-facing fields at a point in time.
- `version_number` starts at `1` for the first version of a prompt and increments by `1` per new version (including rollback-created versions).
- Historical versions (rows of `PromptVersion`) are never mutated after creation.
- The current prompt corresponds to the latest version by `version_number` for that `prompt_id`.

### 3.2 Storage Changes

Extend `Storage` with in-memory version tracking:

- Internal structure: `_prompt_versions: Dict[str, List[PromptVersion]]` keyed by `prompt_id`.
- New methods:
  - `add_prompt_version(version: PromptVersion) -> PromptVersion`
  - `get_prompt_versions(prompt_id: str) -> List[PromptVersion]`
  - `get_prompt_version(prompt_id: str, version_id: str) -> Optional[PromptVersion]`

Version creation must be called by:
- `create_prompt()`
- `update_prompt()` (PUT)
- `patch_prompt()` (PATCH)
- rollback endpoint after `storage.update_prompt()`

Each call logs the *resulting* state of the prompt. `version_number` is assigned as `len(_prompt_versions[prompt_id]) + 1` at creation time.

---

## 4. API Endpoints

### 4.1 List versions for a prompt

- **Method/Path**: `GET /prompts/{prompt_id}/versions`
- **Purpose**: List all versions for a prompt (newest first by `created_at`).

Request:
- Path: `prompt_id: str`

Response (`200 OK`, `PromptVersionList`):

```json
{
  "versions": [
    {
      "id": "ver-1",
      "prompt_id": "prompt-1",
      "title": "Initial title",
      "content": "Initial content",
      "description": "First version",
      "collection_id": null,
      "created_at": "2024-01-01T00:00:00.000000"
    }
  ],
  "total": 1
}
```

Errors:
- `404`: if `storage.get_prompt(prompt_id)` returns `None` → `{"detail": "Prompt not found"}`.
- `422`: only for path binding/validation errors handled by FastAPI/Pydantic.

Example curl:

```bash
curl "http://localhost:8000/prompts/prompt-1/versions"
```

### 4.2 Get a specific version

- **Method/Path**: `GET /prompts/{prompt_id}/versions/{version_id}`

Request:
- Path: `prompt_id: str`, `version_id: str`

Response (`200 OK`, `PromptVersion`):

```json
{
  "id": "ver-1",
  "prompt_id": "prompt-1",
  "title": "Initial title",
  "content": "Initial content",
  "description": "First version",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00.000000"
}
```

Errors:
- `404`: if prompt not found → `{"detail": "Prompt not found"}`.
- `404`: if version not found for that prompt → `{"detail": "Prompt version not found"}`.
- `422`: only for path binding/validation errors handled by FastAPI/Pydantic.

Example curl:

```bash
curl "http://localhost:8000/prompts/prompt-1/versions/ver-1"
```

### 4.3 Roll back to a prior version

- **Method/Path**: `POST /prompts/{prompt_id}/versions/{version_id}/rollback`

Request:
- Path: `prompt_id: str`, `version_id: str`
- Body: none

Response (`200 OK`, updated `Prompt`):

```json
{
  "id": "prompt-1",
  "title": "Initial title",
  "content": "Initial content",
  "description": "First version",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T01:00:00.000000"
}
```

Behavior:
- Validate prompt exists; if not, `404`.
- Validate version belongs to prompt; if not, `404`.
- Create a new `Prompt` instance mirroring the version’s fields but keeping the same `id` and `created_at`, with a new `updated_at`.
- Store via `storage.update_prompt()` and log a new immutable `PromptVersion` snapshot for the rollback state.

Errors:
- `404` prompt not found → `{"detail": "Prompt not found"}`.
- `404` version not found → `{"detail": "Prompt version not found"}`.
- `422`: only for path binding/validation errors handled by FastAPI/Pydantic.

Example curl:

```bash
curl -X POST "http://localhost:8000/prompts/prompt-1/versions/ver-1/rollback"
```
