export default function CollectionList({ collections, selectedId, onSelect }) {
  return (
    <div className="space-y-1">
      {collections.length === 0 ? (
        <p className="text-sm text-gray-500 px-3 py-2">No collections yet. All prompts will appear here.</p>
      ) : (
        collections.map((collection) => (
          <button
            key={collection.id}
            onClick={() => onSelect(collection.id)}
            className={`w-full text-left px-3 py-2 rounded transition-colors ${
              selectedId === collection.id
                ? 'bg-blue-50 text-blue-700 font-medium'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="truncate">{collection.name}</span>
              {collection.prompt_count !== undefined && (
                <span className="text-xs text-gray-500 ml-2">{collection.prompt_count}</span>
              )}
            </div>
            {collection.description && selectedId === collection.id && (
              <p className="text-xs text-gray-600 mt-1">{collection.description}</p>
            )}
          </button>
        ))
      )}
    </div>
  );
}
