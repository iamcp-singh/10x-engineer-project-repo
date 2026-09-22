# PromptLab API Reference

This document describes the current HTTP API implemented by the PromptLab backend.

- Routes: `backend/app/api.py`
- Data models: `backend/app/models.py`

> **Authentication**
>
> Authentication is **not required** for any endpoint in the current
> implementation. All endpoints are open and unauthenticated.

All responses are JSON. Error responses follow FastAPI's standard format:

```json
{
  "detail": "Error message here"
}
```

Timestamps are ISO 8601 strings (UTC), e.g. `"2024-01-01T00:00:00.000000"`.

---

## Data Models (Simplified)

### Prompt

```json
{
  "id": "string",               // auto-generated UUID
  "title": "string",
  "content": "string",
  "description": "string or null",
  "collection_id": "string or null",
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T00:00:00.000000"
}
```

Constraints (from `PromptBase` and related models):

- `title`: required, 1–200 characters
- `content`: required, min length 1
- `description`: optional, max 500 characters
- `collection_id`: optional; when provided in create/update/patch, must refer
  to an existing collection

### Collection

```json
{
  "id": "string",               // auto-generated UUID
  "name": "string",
  "description": "string or null",
  "created_at": "2024-01-01T00:00:00.000000"
}
```

Constraints:

- `name`: required, 1–100 characters
- `description`: optional, max 500 characters

### PromptList

```json
{
  "prompts": [/* Prompt objects */],
  "total": 0
}
```

### CollectionList

```json
{
  "collections": [/* Collection objects */],
  "total": 0
}
```

### HealthResponse

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

(The version value comes from `app.__version__`.)

---

## GET /health

- **Method**: `GET`
- **Path**: `/health`
- **Purpose**: Return basic health information for the API.
- **Authentication**: Not required

### Request

- No path, query, or body parameters.

### Example

```bash
curl http://localhost:8000/health
```

### Success Response

- **Status**: `200 OK`
- **Body** (`HealthResponse`):

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Error Responses

- None specific; the implementation always returns `200` on success.

---

## GET /prompts

- **Method**: `GET`
- **Path**: `/prompts`
- **Purpose**: List prompts with optional collection and text search filters.
- **Authentication**: Not required

### Request

Query parameters (all optional):

- `collection_id` (string): If provided, only prompts whose `collection_id`
  matches this value are returned.
- `search` (string): Case-insensitive search term applied to `title` and
  `description`.

### Example

List all prompts:

```bash
curl "http://localhost:8000/prompts"
```

Filter by collection:

```bash
curl "http://localhost:8000/prompts?collection_id=abcd1234-collection-id"
```

Search by text:

```bash
curl "http://localhost:8000/prompts?search=review"
```

### Success Response

- **Status**: `200 OK`
- **Body** (`PromptList`):

```json
{
  "prompts": [
    {
      "id": "1f8f1b44-1c2d-4c1e-9f3d-123456789abc",
      "title": "Code Review Prompt",
      "content": "Review the following code and provide feedback:\n\n{{code}}",
      "description": "A prompt for AI code review",
      "collection_id": null,
      "created_at": "2024-01-01T00:00:00.000000",
      "updated_at": "2024-01-01T00:00:00.000000"
    }
  ],
  "total": 1
}
```

Notes:

- Prompts are sorted by `created_at` with newest first (`descending=True`).

### Error Responses

- **422 Unprocessable Entity** – only if query parameters cannot be parsed as
  the expected types (handled by FastAPI/Pydantic).

---

## GET /prompts/{id}

- **Method**: `GET`
- **Path**: `/prompts/{id}`
- **Purpose**: Retrieve a single prompt by its ID.
- **Authentication**: Not required

### Request

Path parameters:

- `id` (string): ID of the prompt to retrieve.

### Example

```bash
curl "http://localhost:8000/prompts/1f8f1b44-1c2d-4c1e-9f3d-123456789abc"
```

### Success Response

- **Status**: `200 OK`
- **Body** (`Prompt`):

```json
{
  "id": "1f8f1b44-1c2d-4c1e-9f3d-123456789abc",
  "title": "Code Review Prompt",
  "content": "Review the following code and provide feedback:\n\n{{code}}",
  "description": "A prompt for AI code review",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T00:00:00.000000"
}
```

### Error Responses

- **404 Not Found** – prompt does not exist.

  ```bash
  curl -i "http://localhost:8000/prompts/nonexistent-id"
  ```

  ```json
  {
    "detail": "Prompt not found"
  }
  ```

---

## POST /prompts

- **Method**: `POST`
- **Path**: `/prompts`
- **Purpose**: Create a new prompt.
- **Authentication**: Not required

### Request

JSON body (`PromptCreate`):

```json
{
  "title": "Code Review Prompt",
  "content": "Review the following code and provide feedback:\n\n{{code}}",
  "description": "A prompt for AI code review",
  "collection_id": "optional-collection-id-or-null"
}
```

Constraints:

- `title`: required, 1–200 chars
- `content`: required, min length 1
- `description`: optional, max 500 chars
- `collection_id`: optional; if provided, must refer to an existing collection

### Example

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review Prompt",
    "content": "Review the following code and provide feedback:\n\n{{code}}",
    "description": "A prompt for AI code review"
  }'
```

### Success Response

- **Status**: `201 Created`
- **Body** (`Prompt`):

```json
{
  "id": "9ce74dd8-8b3e-4c02-9f6d-123456789abc",
  "title": "Code Review Prompt",
  "content": "Review the following code and provide feedback:\n\n{{code}}",
  "description": "A prompt for AI code review",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T00:00:00.000000"
}
```

### Error Responses

- **400 Bad Request** – `collection_id` refers to a non-existent collection.

  ```json
  {
    "detail": "Collection not found"
  }
  ```

- **422 Unprocessable Entity** – validation errors on the body (e.g., missing
  required fields), handled by FastAPI/Pydantic.

---

## PUT /prompts/{id}

- **Method**: `PUT`
- **Path**: `/prompts/{id}`
- **Purpose**: Fully replace an existing prompt with new data.
- **Authentication**: Not required

### Request

Path parameters:

- `id` (string): ID of the prompt to update.

JSON body (`PromptUpdate`):

```json
{
  "title": "Updated Title",
  "content": "Updated content for the prompt",
  "description": "Updated description",
  "collection_id": "optional-collection-id-or-null"
}
```

All fields are required in the body for a PUT.

### Example

```bash
curl -X PUT "http://localhost:8000/prompts/9ce74dd8-8b3e-4c02-9f6d-123456789abc" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content for the prompt",
    "description": "Updated description",
    "collection_id": null
  }'
```

### Success Response

- **Status**: `200 OK`
- **Body** (`Prompt`):

```json
{
  "id": "9ce74dd8-8b3e-4c02-9f6d-123456789abc",
  "title": "Updated Title",
  "content": "Updated content for the prompt",
  "description": "Updated description",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T00:00:01.000000"
}
```

### Error Responses

- **404 Not Found** – prompt does not exist.

  ```json
  {
    "detail": "Prompt not found"
  }
  ```

- **400 Bad Request** – `collection_id` refers to a non-existent collection.

  ```json
  {
    "detail": "Collection not found"
  }
  ```

- **422 Unprocessable Entity** – validation errors on the body.

---

## PATCH /prompts/{id}

- **Method**: `PATCH`
- **Path**: `/prompts/{id}`
- **Purpose**: Partially update an existing prompt; only provided fields are
  changed.
- **Authentication**: Not required

### Request

Path parameters:

- `id` (string): ID of the prompt to update.

JSON body (`PromptPatch`): all fields optional.

```json
{
  "title": "Optional new title",
  "content": "Optional new content",
  "description": "Optional new description or null",
  "collection_id": "optional-new-collection-id-or-null"
}
```

Behavior:

- Fields omitted from the body are left unchanged.
- `collection_id`:
  - If omitted: no change.
  - If `null`: prompt is disassociated from any collection.
  - If string: must refer to an existing collection; otherwise, request fails.
- On success, `updated_at` is refreshed to the current time.

### Example – partial title update

```bash
curl -X PATCH "http://localhost:8000/prompts/9ce74dd8-8b3e-4c02-9f6d-123456789abc" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Patched Title"
  }'
```

### Success Response

- **Status**: `200 OK`
- **Body** (`Prompt`):

```json
{
  "id": "9ce74dd8-8b3e-4c02-9f6d-123456789abc",
  "title": "Patched Title",
  "content": "Updated content for the prompt",
  "description": "Updated description",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00.000000",
  "updated_at": "2024-01-01T00:00:02.000000"
}
```

### Error Responses

- **404 Not Found** – prompt does not exist.

  ```json
  {
    "detail": "Prompt not found"
  }
  ```

- **400 Bad Request** – `collection_id` provided (non-null) but collection does
  not exist.

  ```json
  {
    "detail": "Collection not found"
  }
  ```

- **422 Unprocessable Entity** – invalid values for provided fields (for
  example, too-short title).

---

## DELETE /prompts/{id}

- **Method**: `DELETE`
- **Path**: `/prompts/{id}`
- **Purpose**: Delete a prompt by its ID.
- **Authentication**: Not required

### Request

Path parameters:

- `id` (string): ID of the prompt to delete.

### Example

```bash
curl -X DELETE "http://localhost:8000/prompts/9ce74dd8-8b3e-4c02-9f6d-123456789abc"
```

### Success Response

- **Status**: `204 No Content`
- **Body**: Empty

### Error Responses

- **404 Not Found** – prompt does not exist.

  ```json
  {
    "detail": "Prompt not found"
  }
  ```

---

## GET /collections

- **Method**: `GET`
- **Path**: `/collections`
- **Purpose**: List all collections.
- **Authentication**: Not required

### Request

- No path, query, or body parameters.

### Example

```bash
curl "http://localhost:8000/collections"
```

### Success Response

- **Status**: `200 OK`
- **Body** (`CollectionList`):

```json
{
  "collections": [
    {
      "id": "abcd1234-collection-id",
      "name": "Development",
      "description": "Prompts for development tasks",
      "created_at": "2024-01-01T00:00:00.000000"
    }
  ],
  "total": 1
}
```

### Error Responses

- None specific beyond generic FastAPI errors.

---

## GET /collections/{id}

- **Method**: `GET`
- **Path**: `/collections/{id}`
- **Purpose**: Retrieve a single collection by its ID.
- **Authentication**: Not required

### Request

Path parameters:

- `id` (string): ID of the collection to retrieve.

### Example

```bash
curl "http://localhost:8000/collections/abcd1234-collection-id"
```

### Success Response

- **Status**: `200 OK`
- **Body** (`Collection`):

```json
{
  "id": "abcd1234-collection-id",
  "name": "Development",
  "description": "Prompts for development tasks",
  "created_at": "2024-01-01T00:00:00.000000"
}
```

### Error Responses

- **404 Not Found** – collection does not exist.

  ```json
  {
    "detail": "Collection not found"
  }
  ```

---

## POST /collections

- **Method**: `POST`
- **Path**: `/collections`
- **Purpose**: Create a new collection.
- **Authentication**: Not required

### Request

JSON body (`CollectionCreate`):

```json
{
  "name": "Development",
  "description": "Prompts for development tasks"
}
```

Constraints:

- `name`: required, 1–100 chars
- `description`: optional, max 500 chars

### Example

```bash
curl -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Development",
    "description": "Prompts for development tasks"
  }'
```

### Success Response

- **Status**: `201 Created`
- **Body** (`Collection`):

```json
{
  "id": "abcd1234-collection-id",
  "name": "Development",
  "description": "Prompts for development tasks",
  "created_at": "2024-01-01T00:00:00.000000"
}
```

### Error Responses

- **422 Unprocessable Entity** – validation errors on the body (e.g., missing
  name).

---

## DELETE /collections/{id}

- **Method**: `DELETE`
- **Path**: `/collections/{id}`
- **Purpose**: Delete a collection by its ID.
- **Authentication**: Not required

### Request

Path parameters:

- `id` (string): ID of the collection to delete.

### Behavior

- The endpoint calls `storage.delete_collection(id)`.
- In `Storage.delete_collection`:
  - If the collection exists:
    - All prompts whose `collection_id` equals this ID have their
      `collection_id` set to `null`.
    - The collection is removed from storage.
    - The method returns `True`, and the API responds with `204 No Content`.
  - If the collection does not exist:
    - The method returns `False`, and the API raises a 404 error.

### Example

```bash
curl -X DELETE "http://localhost:8000/collections/abcd1234-collection-id"
```

### Success Response

- **Status**: `204 No Content`
- **Body**: Empty

### Error Responses

- **404 Not Found** – collection does not exist.

  ```json
  {
    "detail": "Collection not found"
  }
  ```
