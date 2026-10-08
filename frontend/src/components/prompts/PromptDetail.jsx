import { useState, useEffect } from 'react';
import { Button, LoadingSpinner, ErrorMessage, Modal } from '../shared';
import { getPrompt, deletePrompt } from '../../api';

export default function PromptDetail({ promptId, onEdit, onDelete, onClose }) {
  const [prompt, setPrompt] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchPrompt();
  }, [promptId]);

  const fetchPrompt = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getPrompt(promptId);
      setPrompt(data);
    } catch (err) {
      setError(err.message || 'Prompt not found or failed to load.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    try {
      setDeleting(true);
      await deletePrompt(promptId);
      onDelete(promptId);
    } catch (err) {
      setError(err.message || "Couldn't delete prompt. Try again.");
      setShowDeleteConfirm(false);
    } finally {
      setDeleting(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading prompt..." />;
  }

  if (error) {
    return (
      <div>
        <ErrorMessage message={error} />
        <div className="mt-4">
          <Button onClick={onClose} variant="secondary">Back</Button>
        </div>
      </div>
    );
  }

  if (!prompt) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{prompt.title}</h1>
        
        {prompt.description && (
          <p className="text-gray-600 mb-4">{prompt.description}</p>
        )}

        {prompt.tags && prompt.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {prompt.tags.map((tag, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Content</h2>
        <div className="bg-gray-50 rounded p-4 whitespace-pre-wrap font-mono text-sm">
          {prompt.content}
        </div>
      </div>

      <div className="flex gap-3">
        <Button onClick={onClose} variant="secondary">Back</Button>
        <Button onClick={() => onEdit(prompt)}>Edit</Button>
        <Button onClick={() => setShowDeleteConfirm(true)} variant="danger">Delete</Button>
      </div>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        title="Delete Prompt"
      >
        <p className="mb-4">Are you sure you want to delete this prompt? This action cannot be undone.</p>
        <div className="flex gap-3 justify-end">
          <Button 
            onClick={() => setShowDeleteConfirm(false)} 
            variant="secondary"
            disabled={deleting}
          >
            Cancel
          </Button>
          <Button 
            onClick={handleDelete} 
            variant="danger"
            disabled={deleting}
          >
            {deleting ? 'Deleting...' : 'Yes, Delete'}
          </Button>
        </div>
      </Modal>
    </div>
  );
}
