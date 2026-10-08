import PromptCard from './PromptCard';
import { LoadingSpinner, ErrorMessage } from '../shared';

export default function PromptList({ prompts, onSelectPrompt, loading, error, emptyMessage }) {
  if (loading) {
    return <LoadingSpinner message="Loading prompts..." />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (prompts.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">
          {emptyMessage || "No prompts yet. Create your first prompt to get started!"}
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {prompts.map((prompt) => (
        <PromptCard 
          key={prompt.id} 
          prompt={prompt} 
          onClick={onSelectPrompt}
        />
      ))}
    </div>
  );
}
