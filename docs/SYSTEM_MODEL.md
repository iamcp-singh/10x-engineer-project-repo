# PromptLab Backend System Model

## 1. Architecture
The backend is a small FastAPI application split across a few main files. `main.py` is used to start the server and imports the FastAPI app from `app/api.py`. The routes and most of the application logic are in `api.py`. The data models and validation rules are defined in `models.py`, while `storage.py` keeps prompts and collections in memory. `utils.py` contains helper functions used for things such as sorting, filtering and searching prompts. The tests are kept separately in the `tests` directory.

## 2. Application Entry Point
`backend/main.py` is the entry point used to start the backend. When `python main.py` is run, the `if __name__ == "__main__":` block starts Uvicorn using the FastAPI `app` imported from `app.api`. The server is configured to listen on `0.0.0.0` on port `8000`, with auto-reload enabled for development.

## 3. API Endpoints
The backend currently exposes the following endpoints:

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Returns the API health status and current version. |
| GET | `/prompts` | Lists prompts, with optional collection filtering and search. |
| GET | `/prompts/{prompt_id}` | Retrieves a prompt by its ID. |
| POST | `/prompts` | Creates a new prompt. |
| PUT | `/prompts/{prompt_id}` | Fully updates an existing prompt. |
| DELETE | `/prompts/{prompt_id}` | Deletes a prompt. |
| GET | `/collections` | Lists all collections. |
| GET | `/collections/{collection_id}` | Retrieves a collection by its ID. |
| POST | `/collections` | Creates a new collection. |
| DELETE | `/collections/{collection_id}` | Deletes a collection. |

At this stage, there is no `PATCH /prompts/{prompt_id}` endpoint in the existing application.

## 4. Request and Data Flow
For a `GET /prompts` request, FastAPI first routes the request to the `list_prompts` function in `api.py`. The function gets the stored prompts from the global `storage` instance by calling `storage.get_all_prompts()`.

If the request contains a `collection_id`, `filter_prompts_by_collection()` is used to filter the results. If a search value is provided, `search_prompts()` searches the prompt title and description. The resulting prompts are then passed through `sort_prompts_by_date()`.

The API puts the prompts and total count into the `PromptList` response model from `models.py`. FastAPI then returns the response to the client with a `200 OK` status.

For creating a prompt, the flow is similar: the request is validated using `PromptCreate`, a `Prompt` object is created, and it is passed to `storage.create_prompt()` where it is stored in memory before being returned to the client. 

## 5. Prompt and Collection Relationship**

A prompt can optionally belong to a collection through its `collection_id` field. The field stores the ID of the collection rather than the collection object itself. Since the field is optional, a prompt can also exist without a collection.

Multiple prompts can have the same `collection_id`, so one collection can be associated with multiple prompts. There is no separate database foreign key enforcing this relationship because the application uses in-memory Python dictionaries for storage. The API checks that a collection exists when creating or updating a prompt with a `collection_id`.

When a collection is deleted, the storage layer sets the `collection_id` of prompts belonging to that collection to `None` before deleting the collection. This prevents prompts from retaining a reference to a collection that no longer exists.

## 6. Storage Layer
The application uses an in-memory `Storage` class in `storage.py` instead of a database. It keeps prompts in the `_prompts` dictionary and collections in the `_collections` dictionary, using each object's ID as the dictionary key.

The storage class provides methods to create, retrieve, update and delete prompts and collections. It also has a method for getting prompts belonging to a particular collection. The global `storage` instance is shared by the API.

Because the data is only stored in memory, it is lost when the application is stopped or restarted. There is no persistent database storage in the current implementation. When a collection is deleted, the storage layer finds prompts belonging to that collection and clears their `collection_id` before removing the collection. When a collection is deleted, the storage layer finds prompts belonging to that collection and clears their `collection_id` before removing the collection.

## 7. Utility Functions
`utils.py` contains helper functions used by the API when working with prompts.

`sort_prompts_by_date()` sorts prompts using their `created_at` value and supports descending order, which is used by the API to return newest prompts first.

The file also contains `validate_prompt_content()`, which checks whether prompt content meets the required rules, and `extract_variables()`, which finds template variables in prompt content using the `{{variable_name}}` format.

## 8. External Dependencies
The backend depends on FastAPI for the web API, Uvicorn for running the application server, and Pydantic for the data models and validation.

The project also uses pytest for testing, pytest-cov for test coverage, and httpx for the API test client used by the tests. The specific versions are listed in `backend/requirements.txt`.

## 9. Context Strategy
I started the exploration with the whole backend repository because I was not familiar with the project and needed to understand where the main parts of the application were and how they related to each other.

After getting the high-level picture, I narrowed the context for specific questions. For example, I used `api.py`, `storage.py` and `models.py` when looking at the prompt creation and collection deletion flows because those files were directly involved. I used only `storage.py` when I wanted to understand how data was stored, and only `models.py` when looking at the Prompt and Collection relationship. I also used only `utils.py` when investigating sorting, filtering and searching.

For the final architecture understanding, I brought the main backend files together again because I needed to see how the individual components connected. Using narrower context for specific questions helped avoid unrelated code while still using the wider context when understanding the overall system.