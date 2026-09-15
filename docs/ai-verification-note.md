# AI Verification Note

## AI mistake: Describing the collection deletion cleanup as atomic

During the exploration of the collection deletion behaviour, the AI recommended moving the cleanup logic into the Storage layer. It described the cleanup as an “atomic operation”.

I verified this description against the actual `storage.py` implementation and found that this was not fully accurate. The project uses plain in-memory Python dictionaries to store prompts and collections. There is no database transaction, rollback mechanism, or other transaction system that provides an atomicity guarantee.

The actual implementation simply finds the prompts belonging to the collection, sets their `collection_id` to `None`, and then deletes the collection from the in-memory collections dictionary.

I detected the issue by checking the source code rather than accepting the AI's description of the operation. I therefore kept the implementation simple and limited it to the existing Storage layer, using the existing `get_prompts_by_collection()` method.