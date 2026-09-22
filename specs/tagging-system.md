# Tagging System Specification

## 1. Overview and Goals

The tagging system adds simple, string-based labels to prompts to improve organization and filtering while keeping the existing Prompt model and API patterns. Tags live on the Prompt model and are managed and queried via FastAPI endpoints consistent with current error-handling conventions.

Goals:
- Allow each prompt to have zero or more tags.
- Provide APIs to add, remove, and query by tags.
- Make behavior predictable and testable with clear validation and edge-case rules.

---

## 2. User Stories & Acceptance Criteria

### US1: Add tags to a prompt

As a user, I can add tags to an existing prompt.

Acceptance criteria:
- Given an existing prompt, `POST /prompts/{id}/tags` with a non-empty `tags` list of valid strings returns `200` and a `Prompt` whose `tags` field is the union of old and new tags (no duplicates), and `updated_at` changed.
- Given a non-existent prompt ID, `POST /prompts/{id}/tags` returns `404` with `{"detail": "Prompt not found"}`.
- Given a body where any tag is empty or only whitespace, the endpoint returns `422` via Pydantic validation.

### US2: Remove tags from a prompt

As a user, I can remove specific tags from a prompt.

Acceptance criteria:
- Given an existing prompt, `DELETE /prompts/{id}/tags` with `tags` containing one or more existing tags returns `200` and a `Prompt` where those tags are removed and `updated_at` changed.
- Removing tags that do not exist on the prompt still returns `200` with the original tags unchanged and an updated `updated_at`.
- Given a non-existent prompt ID, the endpoint returns `404` with `{"detail": "Prompt not found"}`.

### US3: Filter prompts by tags

As a user, I can list prompts that match a set of tags.

Acceptance criteria:
- `GET /prompts?tags=tag1,tag2` returns `200` and only prompts whose `tags` array contains **all** specified tags, with `total` equal to the number of returned prompts.
- Given a tags filter that matches no prompts, the response is `200` with `prompts: []` and `total: 0`.
- Given an empty `tags` query value (e.g., `tags=`), behavior is the same as omitting `tags` (no tag filter applied).

---

## 3. Data Model Changes

### 3.1 Prompt model extensions

Extend `PromptBase` and related models in `models.py`:

```python
class PromptBase(BaseModel):
    title: str
    content: str
    description: Optional[str]
    collection_id: Optional[str]
    tags: List[str] = Field(default_factory=list, max_items=50)

class PromptCreate(PromptBase):
    pass

class PromptUpdate(PromptBase):
    pass

class PromptPatch(BaseModel):
    title: Optional[str]
    content: Optional[str]
    description: Optional[str]
    collection_id: Optional[str]
    tags: Optional[List[str]] = Field(default=None, max_items=50)
```

Validation rules for tags:
- Tag length: `1`–`50` characters after trimming whitespace.
- Empty or whitespace-only tags are invalid (`422`).
- Maximum tags per prompt: 50; exceeding this in create/update/patch/add operations yields `422`.
- Case-sensitive: `"Review"` and `"review"` are different tags.
- Duplicates within a single request body are allowed in input but result in a unique set on the stored `Prompt`.

Implementation detail (schema-only): define a custom validator on `PromptBase.tags` and `PromptPatch.tags` to strip whitespace, reject empty, and enforce length.

### 3.2 Storage

No new storage structures are required; `tags` are stored on `Prompt` instances in `_prompts`.

---

## 4. API Endpoints

### 4.1 Add tags to a prompt

- **Method/Path**: `POST /prompts/{prompt_id}/tags`
- **Purpose**: Add tags to a prompt, merging with existing tags.

Request:
- Path: `prompt_id: str`
- Body:

```json
{
  "tags": ["review", "backend"]
}
```

Response (`200 OK`, `Prompt`):

```json
{
  "id": "prompt-1",
  "title": "Code Review Prompt",
  "content": "...",
  "description": "...",
  "collection_id": null,
  "tags": ["review", "backend"],
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T00:00:01.000000"
}
```

Behavior:
- If the prompt already has tags, the resulting `tags` is `sorted` or stable-union (implementation-defined) of existing and new tags without duplicates.
- `updated_at` is set via `get_current_time()`.

Errors:
- `404`: prompt not found → `{"detail": "Prompt not found"}`.
- `422`: if `tags` is missing, empty list, or contains invalid strings (too long, empty/whitespace).

Example curl:

```bash
curl -X POST "http://localhost:8000/prompts/prompt-1/tags" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["review", "backend"]}'
```

### 4.2 Remove tags from a prompt

- **Method/Path**: `DELETE /prompts/{prompt_id}/tags`
- **Purpose**: Remove specified tags from a prompt.

Request:
- Path: `prompt_id: str`
- Body:

```json
{
  "tags": ["backend"]
}
```

Response (`200 OK`, `Prompt`):

```json
{
  "id": "prompt-1",
  "title": "Code Review Prompt",
  "content": "...",
  "description": "...",
  "collection_id": null,
  "tags": ["review"],
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T00:05:00.000000"
}
```

Behavior:
- All tags in the request body are removed from the prompt’s `tags` if present.
- Tags not present on the prompt are ignored; the endpoint still returns `200`.
- If the resulting tag list would exceed 50 items (not possible when removing), no additional validation is required.

Errors:
- `404`: prompt not found → `{"detail": "Prompt not found"}`.
- `422`: if `tags` list is missing or contains invalid strings.

Example curl:

```bash
curl -X DELETE "http://localhost:8000/prompts/prompt-1/tags" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["backend"]}'
```

### 4.3 Filter prompts by tags

- **Method/Path**: `GET /prompts?tags=tag1,tag2`
- **Purpose**: List prompts whose `tags` contain **all** specified tags.

Request:
- Query: `tags` – comma-separated tag string, e.g. `tags=review,backend`.

Response (`200 OK`, `PromptList`):

```json
{
  "prompts": [
    {
      "id": "prompt-1",
      "title": "Code Review Prompt",
      "content": "...",
      "description": "...",
      "collection_id": null,
      "tags": ["review", "backend"],
      "created_at": "2024-01-01T00:00:00.000000",
      "updated_at": "2024-01-01T00:00:00.000000"
    }
  ],
  "total": 1
}
```

Behavior:
- If `tags` is omitted or an empty string (`tags=`), behavior is identical to the existing `/prompts` list endpoint (no tag-based filtering).
- If `tags` is non-empty, split by comma, trim whitespace on each token, discard empty tokens, and apply ALL semantics: only prompts where every requested tag is present in the prompt’s `tags` array are returned.

Errors:
- `422`: if `tags` query cannot be parsed as a string (unlikely with FastAPI default types, but consistent with current behavior).

Example curl:

```bash
curl "http://localhost:8000/prompts?tags=review,backend"
```
