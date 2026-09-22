"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return basic health information for the API.

    Returns:
        HealthResponse: The current service status and version.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List prompts with optional collection and search filters.

    Args:
        collection_id: Optional ID of a collection to restrict prompts to that
            collection only.
        search: Optional search string to match against prompt titles and
            descriptions (case-insensitive).

    Returns:
        PromptList: A list of prompts matching the filters, sorted by
        creation time with newest prompts first.
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a prompt by its ID.

    Args:
        prompt_id: The unique identifier of the prompt.

    Returns:
        The prompt object if found.

    Raises:
        HTTPException: If no prompt with the given ID exists.
    """
    # BUG #1: This will raise a 500 error if prompt doesn't exist
    # because we're accessing .id on None
    # Should return 404 instead!
    prompt = storage.get_prompt(prompt_id)

    #FIX of BUG #1: Check if prompt is None before accessing its attributes
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # This line causes the bug - accessing attribute on None
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Args:
        prompt_data: The prompt data to create, including title, content,
            optional description, and optional collection ID.

    Returns:
        Prompt: The newly created prompt.

    Raises:
        HTTPException: If a non-existent collection ID is provided.
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Update an existing prompt fully.

    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: The full prompt data for the update.

    Returns:
        The updated prompt object.

    Raises:
        HTTPException: If the prompt is not found or the collection is not found.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2: We're not updating the updated_at timestamp!
    # The updated prompt keeps the old timestamp
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # FIX: call the helper function here
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Partially update an existing prompt.

    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: The partial prompt data for the update.

    Returns:
        The updated prompt object.

    Raises:
        HTTPException: If the prompt is not found or the collection is not found.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    update_data = prompt_data.model_dump(exclude_unset=True)

    if "collection_id" in update_data:
        new_col_id = update_data["collection_id"]
        if new_col_id is not None:
            collection = storage.get_collection(new_col_id)
            if not collection:
                raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = existing.model_copy(update=update_data)
    updated_prompt.updated_at = get_current_time()

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by its ID.

    Args:
        prompt_id: The unique identifier of the prompt to delete.

    Returns:
        None: Returns an empty response body with HTTP 204 on success.

    Raises:
        HTTPException: If no prompt with the given ID exists.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.

    Returns:
        CollectionList: All collections currently stored, along with the
        total number of collections.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by its ID.

    Args:
        collection_id: The unique identifier of the collection to retrieve.

    Returns:
        Collection: The matching collection.

    Raises:
        HTTPException: If no collection with the given ID exists.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data: The collection data to create, including name and
            optional description.

    Returns:
        Collection: The newly created collection.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection by its ID.

    Deletion also updates any prompts that reference this collection in the
    in-memory storage layer so they no longer point to the deleted collection.

    Args:
        collection_id: The unique identifier of the collection to delete.

    Returns:
        None: Returns an empty response body with HTTP 204 on success.

    Raises:
        HTTPException: If no collection with the given ID exists.
    """
    # BUG #4: We delete the collection but don't handle the prompts!
    # Prompts with this collection_id become orphaned with invalid reference
    # Should either: delete the prompts, set collection_id to None, or prevent deletion
    
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Missing: Handle prompts that belong to this collection!
    
    return None
