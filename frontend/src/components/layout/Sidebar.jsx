export default function Sidebar({ collections, selectedId, onSelectCollection }) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-screen p-4 hidden md:block">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Collections</h2>
      
      <nav>
        <button
          onClick={() => onSelectCollection(null)}
          className={`w-full text-left px-3 py-2 rounded mb-1 transition-colors ${
            selectedId === null
              ? 'bg-blue-50 text-blue-700 font-medium'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          All Prompts
        </button>

        {collections.length === 0 ? (
          <p className="text-sm text-gray-500 px-3 py-2">No collections yet</p>
        ) : (
          collections.map((collection) => (
            <button
              key={collection.id}
              onClick={() => onSelectCollection(collection.id)}
              className={`w-full text-left px-3 py-2 rounded mb-1 transition-colors ${
                selectedId === collection.id
                  ? 'bg-blue-50 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <div className="flex items-center justify-between">
                <span>{collection.name}</span>
                {collection.prompt_count !== undefined && (
                  <span className="text-xs text-gray-500">{collection.prompt_count}</span>
                )}
              </div>
            </button>
          ))
        )}
      </nav>
    </aside>
  );
}
