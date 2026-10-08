"""Tests for prompt versioning feature"""

from datetime import datetime

import pytest

from app.models import Prompt, PromptVersion


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
