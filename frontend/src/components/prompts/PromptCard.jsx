export default function PromptCard({ prompt, onClick }) {
  const contentPreview = prompt.content.length > 100 
    ? prompt.content.substring(0, 100) + '...' 
    : prompt.content;

  return (
    <div
      onClick={() => onClick(prompt.id)}
      className="bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer p-4 border border-gray-200"
    >
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{prompt.title}</h3>
      
      {prompt.description && (
        <p className="text-sm text-gray-600 mb-2">{prompt.description}</p>
      )}
      
      <p className="text-gray-700 mb-3">{contentPreview}</p>

      {prompt.tags && prompt.tags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {prompt.tags.map((tag, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
