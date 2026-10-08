"""Tests for prompt versioning feature"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.models import Prompt, PromptVersion
from app.storage import Storage, storage


class TestPromptVersionModel:
    """Test PromptVersion model validation and creation"""

    def test_create_prompt_version(self):
        """Test creating a basic prompt version"""
        version = PromptVersion(
            prompt_id="prompt-123",
            title="Test Prompt",
            content="This is test content",
            description="Test description",
            collection_id=None,
            version_number=1,
        )

        assert version.prompt_id == "prompt-123"
        assert version.title == "Test Prompt"
        assert version.content == "This is test content"
        assert version.version_number == 1
        assert version.id is not None
        assert isinstance(version.created_at, datetime)

    def test_version_requires_prompt_id(self):
        """Test that prompt_id is required"""
        with pytest.raises(ValueError):
            PromptVersion(
                title="Test",
                content="Content",
                version_number=1,
            )

    def test_version_number_is_required(self):
        """Test that version_number is required"""
        with pytest.raises(ValueError):
            PromptVersion(
                prompt_id="prompt-123",
                title="Test",
                content="Content",
            )


class TestVersionStorage:
    """Test storage operations for versions"""

    def test_add_prompt_version(self):
        """Test adding a version to storage"""
        storage = Storage()
        
        # Create a prompt first
        prompt = Prompt(
            title="Test Prompt",
            content="Test content",
        )
        storage.create_prompt(prompt)
        
        # Create and add a version
        version = PromptVersion(
            prompt_id=prompt.id,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=prompt.collection_id,
            version_number=1,
        )
        
        result = storage.add_prompt_version(version)
        
        assert result.id == version.id
        assert result.prompt_id == prompt.id
        assert result.version_number == 1

    def test_get_prompt_versions(self):
        """Test retrieving all versions for a prompt"""
        storage = Storage()
        
        prompt = Prompt(title="Test", content="Content")
        storage.create_prompt(prompt)
        
        # Add two versions
        v1 = PromptVersion(
            prompt_id=prompt.id,
            title="Version 1",
            content="Content 1",
            version_number=1,
        )
        v2 = PromptVersion(
            prompt_id=prompt.id,
            title="Version 2",
            content="Content 2",
            version_number=2,
        )
        
        storage.add_prompt_version(v1)
        storage.add_prompt_version(v2)
        
        versions = storage.get_prompt_versions(prompt.id)
        
        assert len(versions) == 2
        # Should be newest first
        assert versions[0].version_number == 2
        assert versions[1].version_number == 1

    def test_get_prompt_version_by_id(self):
        """Test getting a specific version"""
        storage = Storage()
        
        prompt = Prompt(title="Test", content="Content")
        storage.create_prompt(prompt)
        
        version = PromptVersion(
            prompt_id=prompt.id,
            title="Test",
            content="Content",
            version_number=1,
        )
        storage.add_prompt_version(version)
        
        result = storage.get_prompt_version(prompt.id, version.id)
        
        assert result is not None
        assert result.id == version.id
        assert result.version_number == 1

    def test_get_prompt_version_not_found(self):
        """Test getting non-existent version returns None"""
        storage = Storage()
        
        prompt = Prompt(title="Test", content="Content")
        storage.create_prompt(prompt)
        
        result = storage.get_prompt_version(prompt.id, "nonexistent")
        
        assert result is None


class TestVersionAPI:
    """Test version API endpoints"""

    def setup_method(self):
        """Clear storage before each test"""
        storage.clear()
        self.client = TestClient(app)

    def test_list_versions_for_prompt(self):
        """Test GET /prompts/{id}/versions returns all versions"""
        # Create a prompt
        response = self.client.post(
            "/prompts",
            json={
                "title": "Test Prompt",
                "content": "Initial content",
                "description": "Test description",
            },
        )
        assert response.status_code == 201
        prompt_id = response.json()["id"]

        # Manually add versions (in real implementation, these would be auto-created)
        v1 = PromptVersion(
            prompt_id=prompt_id,
            title="Test Prompt",
            content="Initial content",
            description="Test description",
            collection_id=None,
            version_number=1,
        )
        v2 = PromptVersion(
            prompt_id=prompt_id,
            title="Updated Prompt",
            content="Updated content",
            description="Test description",
            collection_id=None,
            version_number=2,
        )
        storage.add_prompt_version(v1)
        storage.add_prompt_version(v2)

        # Get versions
        response = self.client.get(f"/prompts/{prompt_id}/versions")
        
        assert response.status_code == 200
        data = response.json()
        assert "versions" in data
        assert "total" in data
        assert data["total"] == 2
        assert len(data["versions"]) == 2
        # Should be newest first
        assert data["versions"][0]["version_number"] == 2
        assert data["versions"][1]["version_number"] == 1

    def test_list_versions_prompt_not_found(self):
        """Test GET /prompts/{id}/versions returns 404 for non-existent prompt"""
        response = self.client.get("/prompts/nonexistent-id/versions")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_list_versions_empty(self):
        """Test GET /prompts/{id}/versions returns empty list when no versions"""
        # Create a prompt
        response = self.client.post(
            "/prompts",
            json={
                "title": "Test Prompt",
                "content": "Content",
            },
        )
        prompt_id = response.json()["id"]

        # Get versions (none exist yet)
        response = self.client.get(f"/prompts/{prompt_id}/versions")
        
        assert response.status_code == 200
        data = response.json()
        assert data["versions"] == []
        assert data["total"] == 0

    def test_get_specific_version(self):
        """Test GET /prompts/{id}/versions/{version_id} returns specific version"""
        # Create a prompt
        response = self.client.post(
            "/prompts",
            json={"title": "Test", "content": "Content"},
        )
        prompt_id = response.json()["id"]

        # Add a version
        version = PromptVersion(
            prompt_id=prompt_id,
            title="Test",
            content="Content",
            version_number=1,
        )
        storage.add_prompt_version(version)

        # Get the specific version
        response = self.client.get(f"/prompts/{prompt_id}/versions/{version.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == version.id
        assert data["prompt_id"] == prompt_id
        assert data["version_number"] == 1

    def test_get_specific_version_prompt_not_found(self):
        """Test GET /prompts/{id}/versions/{version_id} returns 404 if prompt not found"""
        response = self.client.get("/prompts/bad-id/versions/version-id")

        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_get_specific_version_not_found(self):
        """Test GET /prompts/{id}/versions/{version_id} returns 404 if version not found"""
        # Create a prompt
        response = self.client.post(
            "/prompts",
            json={"title": "Test", "content": "Content"},
        )
        prompt_id = response.json()["id"]

        # Try to get non-existent version
        response = self.client.get(f"/prompts/{prompt_id}/versions/bad-version-id")

        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt version not found"

    def test_rollback_to_version(self):
        """Test POST /prompts/{id}/versions/{version_id}/rollback"""
        # Create a prompt
        response = self.client.post(
            "/prompts",
            json={
                "title": "Original Title",
                "content": "Original content",
                "description": "Original description",
            },
        )
        assert response.status_code == 201
        prompt_id = response.json()["id"]
        original_created_at = response.json()["created_at"]

        # Add a version (simulating what would be auto-created)
        old_version = PromptVersion(
            prompt_id=prompt_id,
            title="Original Title",
            content="Original content",
            description="Original description",
            collection_id=None,
            version_number=1,
        )
        storage.add_prompt_version(old_version)

        # Update the prompt
        response = self.client.put(
            f"/prompts/{prompt_id}",
            json={
                "title": "Updated Title",
                "content": "Updated content",
                "description": "Updated description",
                "collection_id": None,
                "tags": [],
            },
        )
        assert response.status_code == 200

        # Rollback to the old version
        response = self.client.post(
            f"/prompts/{prompt_id}/versions/{old_version.id}/rollback"
        )

        assert response.status_code == 200
        data = response.json()
        # Should have same ID and created_at
        assert data["id"] == prompt_id
        assert data["created_at"] == original_created_at
        # Should have old version's content
        assert data["title"] == "Original Title"
        assert data["content"] == "Original content"
        assert data["description"] == "Original description"
        # updated_at should be newer
        assert data["updated_at"] > old_version.created_at.isoformat()

    def test_rollback_prompt_not_found(self):
        """Test POST /prompts/{id}/versions/{version_id}/rollback with bad prompt ID"""
        response = self.client.post("/prompts/bad-id/versions/version-id/rollback")

        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_rollback_version_not_found(self):
        """Test POST /prompts/{id}/versions/{version_id}/rollback with bad version ID"""
        # Create a prompt
        response = self.client.post(
            "/prompts",
            json={"title": "Test", "content": "Content"},
        )
        prompt_id = response.json()["id"]

        # Try to rollback to non-existent version
        response = self.client.post(
            f"/prompts/{prompt_id}/versions/bad-version-id/rollback"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt version not found"
