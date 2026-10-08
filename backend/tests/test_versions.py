"""Tests for prompt versioning feature"""

from datetime import datetime

import pytest

from app.models import Prompt, PromptVersion
from app.storage import Storage


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
        with pytest.raises(Exception):
            PromptVersion(
                title="Test",
                content="Content",
                version_number=1,
            )

    def test_version_number_is_required(self):
        """Test that version_number is required"""
        with pytest.raises(Exception):
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
