"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """In-memory storage for prompts and collections.

    This class provides a simple in-memory implementation for managing prompts
    and collections. It is intended for development and testing and can be
    replaced with a persistent storage implementation in production.
    """

    def __init__(self):
        """Initialize empty in-memory stores for prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt.

        Args:
            prompt: The Prompt instance to store.

        Returns:
            Prompt: The same Prompt instance after storing it.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.

        Args:
            prompt_id: The unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The matching prompt if found, otherwise None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Return all stored prompts.

        Returns:
            List[Prompt]: A list of all prompts currently stored.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Replace an existing prompt with a new value.

        Args:
            prompt_id: The ID of the prompt to update.
            prompt: The new Prompt instance to store for the given ID.

        Returns:
            Optional[Prompt]: The updated prompt if the ID exists, otherwise
            None.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its ID.

        Args:
            prompt_id: The ID of the prompt to delete.

        Returns:
            bool: True if a prompt with the given ID was deleted, False
            otherwise.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection.

        Args:
            collection: The Collection instance to store.

        Returns:
            Collection: The same Collection instance after storing it.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        Args:
            collection_id: The unique identifier of the collection to
                retrieve.

        Returns:
            Optional[Collection]: The matching collection if found, otherwise
            None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Return all stored collections.

        Returns:
            List[Collection]: A list of all collections currently stored.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection and nullify its reference in linked prompts.

        Args:
            collection_id: The ID of the collection to delete.

        Returns:
            True if the collection was deleted, False otherwise.
        """
        if collection_id in self._collections:
            # Nullify collection_id for all prompts in this collection
            for prompt in self.get_prompts_by_collection(collection_id):
                prompt.collection_id = None
                
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Return all prompts that belong to a given collection.

        Args:
            collection_id: The ID of the collection whose prompts should be
                returned.

        Returns:
            List[Prompt]: A list of prompts associated with the given
            collection ID.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Remove all prompts and collections from storage."""
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
