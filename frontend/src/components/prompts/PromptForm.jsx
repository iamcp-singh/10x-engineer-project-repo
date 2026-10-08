import { useState, useEffect } from 'react';
import { Button, ErrorMessage } from '../shared';

export default function PromptForm({ promptId = null, onSuccess, onCancel }) {
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    description: '',
    collection_id: '',
    tags: '',
  });
  
  const [collections, setCollections] = useState([]);
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetchingPrompt, setFetchingPrompt] = useState(false);

  useEffect(() => {
    fetchCollections();
    if (promptId) {
      fetchPrompt();
    }
  }, [promptId]);

  const fetchCollections = async () => {
    try {
      const response = await fetch('http://localhost:8000/collections');
      if (response.ok) {
        const data = await response.json();
        setCollections(data.collections || []);
      }
    } catch (err) {
      console.error('Failed to fetch collections:', err);
    }
  };

  const fetchPrompt = async () => {
    try {
      setFetchingPrompt(true);
      const response = await fetch(`http://localhost:8000/prompts/${promptId}`);
      
      if (!response.ok) {
        throw new Error('Failed to load prompt');
      }
      
      const data = await response.json();
      setFormData({
        title: data.title || '',
        content: data.content || '',
        description: data.description || '',
        collection_id: data.collection_id || '',
        tags: data.tags ? data.tags.join(', ') : '',
      });
    } catch (err) {
      setSubmitError(err.message || 'Failed to load prompt for editing');
    } finally {
      setFetchingPrompt(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    const newErrors = {};
    
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    
    if (!formData.content.trim()) {
      newErrors.content = 'Content is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    try {
      setLoading(true);
      setSubmitError(null);

      const payload = {
        title: formData.title.trim(),
        content: formData.content.trim(),
        description: formData.description.trim() || null,
        collection_id: formData.collection_id || null,
        tags: formData.tags 
          ? formData.tags.split(',').map(t => t.trim()).filter(t => t.length > 0)
          : [],
      };

      const url = promptId 
        ? `http://localhost:8000/prompts/${promptId}`
        : 'http://localhost:8000/prompts';
      
      const method = promptId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to save prompt');
      }

      const savedPrompt = await response.json();
      onSuccess(savedPrompt);
    } catch (err) {
      setSubmitError(err.message || 'Failed to save. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (fetchingPrompt) {
    return <div className="text-center py-4">Loading prompt...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {submitError && (
        <ErrorMessage message={submitError} onDismiss={() => setSubmitError(null)} />
      )}

      {/* Title */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.title ? 'border-red-500' : 'border-gray-300'
          }`}
          disabled={loading}
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-600">{errors.title}</p>
        )}
      </div>

      {/* Content */}
      <div>
        <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">
          Content <span className="text-red-500">*</span>
        </label>
        <textarea
          id="content"
          name="content"
          value={formData.content}
          onChange={handleChange}
          rows={8}
          className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm ${
            errors.content ? 'border-red-500' : 'border-gray-300'
          }`}
          disabled={loading}
        />
        {errors.content && (
          <p className="mt-1 text-sm text-red-600">{errors.content}</p>
        )}
      </div>

      {/* Description */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
      </div>

      {/* Collection */}
      <div>
        <label htmlFor="collection_id" className="block text-sm font-medium text-gray-700 mb-1">
          Collection
        </label>
        <select
          id="collection_id"
          name="collection_id"
          value={formData.collection_id}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        >
          <option value="">None</option>
          {collections.map((collection) => (
            <option key={collection.id} value={collection.id}>
              {collection.name}
            </option>
          ))}
        </select>
      </div>

      {/* Tags */}
      <div>
        <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-1">
          Tags <span className="text-sm text-gray-500">(comma-separated)</span>
        </label>
        <input
          type="text"
          id="tags"
          name="tags"
          value={formData.tags}
          onChange={handleChange}
          placeholder="example, ai, template"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
      </div>

      {/* Buttons */}
      <div className="flex gap-3 pt-2">
        <Button
          type="button"
          onClick={onCancel}
          variant="secondary"
          disabled={loading}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={loading}
        >
          {loading ? 'Saving...' : (promptId ? 'Update' : 'Create')}
        </Button>
      </div>
    </form>
  );
}
