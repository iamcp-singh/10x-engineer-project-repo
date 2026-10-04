"""Tests for utility functions."""

import pytest
from datetime import timedelta
from app.utils import (
    extract_variables,
    validate_prompt_content,
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts
)
from app.models import Prompt, get_current_time


class TestValidatePromptContent:
    """Test content validation rules."""
    
    def test_validate_valid_content(self):
        """Test valid content passes validation."""
        result = validate_prompt_content("This is a valid prompt content")
        assert result is True

    def test_validate_empty_string(self):
        """Test empty string fails validation."""
        result = validate_prompt_content("")
        assert result is False
    
    def test_validate_whitespace_only(self):
        """Test whitespace-only content fails validation."""
        result = validate_prompt_content("   \n  \t  ")
        assert result is False
    
    def test_validate_too_short(self):
        """Test content less than 10 chars fails."""
        result = validate_prompt_content("short")
        assert result is False
    
    def test_validate_exactly_10_chars(self):
        """Test exactly 10 chars passes validation."""
        result = validate_prompt_content("1234567890")
        assert result is True


class TestExtractVariables:
    """Test variable extraction from prompt templates."""
    
    def test_extract_single_variable(self):
        """Test extracting single {{variable}} from content."""
        content = "Here is a {{code}} snippet"
        result = extract_variables(content)
        assert result == ["code"]
    
    def test_extract_multiple_variables(self):
        """Test extracting multiple variables."""
        content = "Review {{code}} for {{language}}"
        result = extract_variables(content)
        assert result == ["code", "language"]
    
    def test_extract_no_variables(self):
        """Test content with no variables returns empty list."""
        content = "No variables here"
        result = extract_variables(content)
        assert result == []
    
    def test_extract_empty_content(self):
        """Test empty content returns empty list."""
        result = extract_variables("")
        assert result == []


class TestSortPromptsByDate:
    """Test sorting prompts by creation date."""
    
    def test_sort_descending_newest_first(self, sample_prompt_data):
        """Test that descending=True returns newest first."""
        now = get_current_time()
        old = Prompt(
            **sample_prompt_data,
            created_at=now - timedelta(hours=1)
        )
        new = Prompt(
            **sample_prompt_data,
            created_at=now
        )
        
        prompts = [old, new]
        sorted_prompts = sort_prompts_by_date(prompts, descending=True)
        
        assert sorted_prompts[0].id == new.id
        assert sorted_prompts[1].id == old.id
    
    def test_sort_ascending_oldest_first(self, sample_prompt_data):
        """Test that descending=False returns oldest first."""
        now = get_current_time()
        old = Prompt(
            **sample_prompt_data,
            created_at=now - timedelta(hours=1)
        )
        new = Prompt(
            **sample_prompt_data,
            created_at=now
        )
        
        prompts = [new, old]
        sorted_prompts = sort_prompts_by_date(prompts, descending=False)
        
        assert sorted_prompts[0].id == old.id
        assert sorted_prompts[1].id == new.id
    
    def test_sort_empty_list(self):
        """Test sorting empty list returns empty list."""
        result = sort_prompts_by_date([], descending=True)
        assert result == []


class TestFilterPromptsByCollection:
    """Test filtering prompts by collection ID."""
    
    def test_filter_matches_collection(self, sample_prompt_data):
        """Test that prompts with matching collection_id are returned."""
        col_id = "collection-1"
        prompt1 = Prompt(
            **sample_prompt_data,
            collection_id=col_id
        )
        prompt2 = Prompt(
            **sample_prompt_data,
            collection_id="collection-2"
        )
        
        prompts = [prompt1, prompt2]
        result = filter_prompts_by_collection(prompts, col_id)
        
        assert len(result) == 1
        assert result[0].id == prompt1.id
    
    def test_filter_no_matches(self, sample_prompt_data):
        """Test filtering returns empty list when no prompts match."""
        prompt = Prompt(
            **sample_prompt_data,
            collection_id="collection-1"
        )
        
        result = filter_prompts_by_collection([prompt], "collection-2")
        assert result == []
    
    def test_filter_empty_list(self):
        """Test filtering empty list returns empty list."""
        result = filter_prompts_by_collection([], "any-id")
        assert result == []


class TestSearchPrompts:
    """Test searching prompts by title and description."""
    
    def test_search_matches_title(self, sample_prompt_data):
        """Test searching for term in title."""
        data = {**sample_prompt_data, "title": "Code Review Prompt"}
        prompt = Prompt(**data)
        
        result = search_prompts([prompt], "Review")
        assert len(result) == 1
    
    def test_search_matches_description(self, sample_prompt_data):
        """Test searching for term in description."""
        data = {**sample_prompt_data, "description": "For code reviews"}
        prompt = Prompt(**data)
        
        result = search_prompts([prompt], "reviews")
        assert len(result) == 1
    
    def test_search_case_insensitive(self, sample_prompt_data):
        """Test search is case-insensitive."""
        data = {**sample_prompt_data, "title": "Code Review"}
        prompt = Prompt(**data)
        
        result = search_prompts([prompt], "code")
        assert len(result) == 1
    
    def test_search_no_match(self, sample_prompt_data):
        """Test search returns empty when no match."""
        data = {**sample_prompt_data, "title": "Something"}
        prompt = Prompt(**data)
        
        result = search_prompts([prompt], "nonexistent")
        assert result == []
    
    def test_search_description_null(self, sample_prompt_data):
        """Test search handles null description gracefully."""
        data = {**sample_prompt_data, "description": None}
        prompt = Prompt(**data)
        
        result = search_prompts([prompt], "anything")
        assert result == []
    
    def test_search_empty_list(self):
        """Test search on empty list returns empty."""
        result = search_prompts([], "anything")
        assert result == []
