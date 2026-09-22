"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.

    Args:
        prompts: A list of prompt objects to sort.
        descending: Whether to sort in descending order (newest first).

    Returns:
        A sorted list of prompt objects.
    """
    # BUG #3: This sorts ascending (oldest first) when it should sort descending (newest first)
    # The 'descending' parameter is ignored!
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.

    Args:
        prompts: A list of prompts to filter.
        collection_id: The collection ID to match against each prompt's
            ``collection_id`` field.

    Returns:
        List[Prompt]: A list of prompts that belong to the specified
        collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title and description text.

    The search is case-insensitive and matches prompts whose title or
    description contains the query string.

    Args:
        prompts: A list of prompts to search within.
        query: The text to search for in the title and description.

    Returns:
        List[Prompt]: A list of prompts where the title or description
        contains the query string.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check whether prompt content meets basic validation rules.

    The content must not be empty or whitespace-only, and the trimmed content
    must be at least 10 characters long.

    Args:
        content: The prompt content to validate.

    Returns:
        bool: True if the content is valid according to the rules, False
        otherwise.
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Variables are expected in the format ``{{variable_name}}`` using
    word characters (``\w``) for the variable name.

    Args:
        content: The prompt content string to scan.

    Returns:
        List[str]: A list of variable names found in the content, without the
        surrounding curly braces.
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
