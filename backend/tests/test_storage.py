"""Tests for storage operations."""

from app.models import Collection, Prompt
from app.storage import storage


class TestStoragePromptCRUD:
    """Test prompt CRUD operations."""

    def test_create_prompt(self, sample_prompt_data):
        """Test creating and storing a prompt."""
        prompt = Prompt(**sample_prompt_data)
        result = storage.create_prompt(prompt)

        assert result.id == prompt.id
        assert result.title == prompt.title

    def test_get_prompt(self, sample_prompt_data):
        """Test retrieving a stored prompt."""
        prompt = Prompt(**sample_prompt_data)
        storage.create_prompt(prompt)

        result = storage.get_prompt(prompt.id)

        assert result is not None
        assert result.id == prompt.id

    def test_get_prompt_not_found(self):
        """Test getting non-existent prompt returns None."""
        result = storage.get_prompt("nonexistent-id")
        assert result is None

    def test_get_all_prompts(self, sample_prompt_data):
        """Test retrieving all prompts."""
        prompt1 = Prompt(**sample_prompt_data)
        prompt2 = Prompt(**sample_prompt_data)

        storage.create_prompt(prompt1)
        storage.create_prompt(prompt2)

        result = storage.get_all_prompts()
        assert len(result) == 2

    def test_update_prompt(self, sample_prompt_data):
        """Test updating an existing prompt."""
        prompt = Prompt(**sample_prompt_data)
        storage.create_prompt(prompt)

        updated_data = {**sample_prompt_data, "title": "Updated Title"}
        updated_prompt = Prompt(id=prompt.id, **updated_data)

        result = storage.update_prompt(prompt.id, updated_prompt)

        assert result is not None
        assert result.title == "Updated Title"

    def test_update_prompt_not_found(self, sample_prompt_data):
        """Test updating non-existent prompt returns None."""
        prompt = Prompt(**sample_prompt_data)
        result = storage.update_prompt("nonexistent-id", prompt)
        assert result is None

    def test_delete_prompt(self, sample_prompt_data):
        """Test deleting a prompt."""
        prompt = Prompt(**sample_prompt_data)
        storage.create_prompt(prompt)

        result = storage.delete_prompt(prompt.id)

        assert result is True
        assert storage.get_prompt(prompt.id) is None

    def test_delete_prompt_not_found(self):
        """Test deleting non-existent prompt returns False."""
        result = storage.delete_prompt("nonexistent-id")
        assert result is False


class TestStorageCollectionCRUD:
    """Test collection CRUD operations."""

    def test_create_collection(self, sample_collection_data):
        """Test creating a collection."""
        collection = Collection(**sample_collection_data)
        result = storage.create_collection(collection)

        assert result.id == collection.id
        assert result.name == collection.name

    def test_get_collection(self, sample_collection_data):
        """Test retrieving a collection."""
        collection = Collection(**sample_collection_data)
        storage.create_collection(collection)

        result = storage.get_collection(collection.id)

        assert result is not None
        assert result.id == collection.id

    def test_get_collection_not_found(self):
        """Test getting non-existent collection returns None."""
        result = storage.get_collection("nonexistent-id")
        assert result is None

    def test_get_all_collections(self, sample_collection_data):
        """Test retrieving all collections."""
        col1 = Collection(**sample_collection_data)
        col2 = Collection(**{**sample_collection_data, "name": "Other"})

        storage.create_collection(col1)
        storage.create_collection(col2)

        result = storage.get_all_collections()
        assert len(result) == 2

    def test_delete_collection(self, sample_collection_data):
        """Test deleting a collection."""
        collection = Collection(**sample_collection_data)
        storage.create_collection(collection)

        result = storage.delete_collection(collection.id)

        assert result is True
        assert storage.get_collection(collection.id) is None

    def test_delete_collection_not_found(self):
        """Test deleting non-existent collection returns False."""
        result = storage.delete_collection("nonexistent-id")
        assert result is False


class TestStoragePersistence:
    """Test persistence of data within session."""

    def test_prompt_persists_across_operations(self, sample_prompt_data):
        """Test prompt remains in storage across operations."""
        prompt = Prompt(**sample_prompt_data)
        storage.create_prompt(prompt)

        retrieved1 = storage.get_prompt(prompt.id)
        assert retrieved1 is not None

        all_prompts = storage.get_all_prompts()
        assert len(all_prompts) == 1

        retrieved2 = storage.get_prompt(prompt.id)
        assert retrieved2.id == prompt.id

    def test_collection_prompt_relationship(
        self, sample_collection_data, sample_prompt_data
    ):
        """Test prompts maintain collection relationship."""
        collection = Collection(**sample_collection_data)
        storage.create_collection(collection)

        prompt_data = {**sample_prompt_data, "collection_id": collection.id}
        prompt = Prompt(**prompt_data)
        storage.create_prompt(prompt)

        retrieved = storage.get_prompt(prompt.id)
        assert retrieved.collection_id == collection.id
