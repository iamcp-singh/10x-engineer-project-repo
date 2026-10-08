import { useState, useEffect } from 'react';
import { Layout, Sidebar } from './components/layout';
import { PromptList, PromptDetail, PromptForm } from './components/prompts';
import { CollectionForm } from './components/collections';
import { Button, Modal, SearchBar } from './components/shared';

function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [selectedCollection, setSelectedCollection] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Modal states
  const [showPromptForm, setShowPromptForm] = useState(false);
  const [showCollectionForm, setShowCollectionForm] = useState(false);
  const [showPromptDetail, setShowPromptDetail] = useState(false);
  const [editingPrompt, setEditingPrompt] = useState(null);
  const [selectedPromptId, setSelectedPromptId] = useState(null);

  useEffect(() => {
    fetchPrompts();
    fetchCollections();
  }, [selectedCollection, searchQuery]);

  const fetchPrompts = async () => {
    try {
      setLoading(true);
      setError(null);
      
      let url = 'http://localhost:8000/prompts';
      const params = new URLSearchParams();
      
      if (searchQuery) {
        params.append('search', searchQuery);
      }
      if (selectedCollection) {
        params.append('collection_id', selectedCollection);
      }
      
      if (params.toString()) {
        url += '?' + params.toString();
      }
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to load prompts');
      }
      
      const data = await response.json();
      setPrompts(data.prompts || []);
    } catch (err) {
      setError("Couldn't load prompts. Try refreshing.");
    } finally {
      setLoading(false);
    }
  };

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

  const handleCreatePrompt = () => {
    setEditingPrompt(null);
    setShowPromptForm(true);
  };

  const handleEditPrompt = (prompt) => {
    setEditingPrompt(prompt);
    setShowPromptDetail(false);
    setShowPromptForm(true);
  };

  const handlePromptSuccess = () => {
    setShowPromptForm(false);
    setEditingPrompt(null);
    fetchPrompts();
  };

  const handleCollectionSuccess = () => {
    setShowCollectionForm(false);
    fetchCollections();
  };

  const handleSelectPrompt = (promptId) => {
    setSelectedPromptId(promptId);
    setShowPromptDetail(true);
  };

  const handleDeletePrompt = () => {
    setShowPromptDetail(false);
    setSelectedPromptId(null);
    fetchPrompts();
  };

  const handleCloseDetail = () => {
    setShowPromptDetail(false);
    setSelectedPromptId(null);
  };

  const getEmptyMessage = () => {
    if (searchQuery) {
      return `No prompts match '${searchQuery}'. Try a different search.`;
    }
    if (selectedCollection) {
      return 'This collection is empty.';
    }
    return "No prompts yet. Create your first prompt to get started!";
  };

  return (
    <Layout
      sidebar={
        <Sidebar
          collections={collections}
          selectedId={selectedCollection}
          onSelectCollection={setSelectedCollection}
        />
      }
    >
      {/* Action Bar */}
      <div className="mb-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <SearchBar onSearch={setSearchQuery} />
        <div className="flex gap-2">
          <Button onClick={() => setShowCollectionForm(true)} variant="secondary">
            New Collection
          </Button>
          <Button onClick={handleCreatePrompt}>
            New Prompt
          </Button>
        </div>
      </div>

      {/* Prompt List or Detail View */}
      {showPromptDetail ? (
        <PromptDetail
          promptId={selectedPromptId}
          onEdit={handleEditPrompt}
          onDelete={handleDeletePrompt}
          onClose={handleCloseDetail}
        />
      ) : (
        <PromptList
          prompts={prompts}
          onSelectPrompt={handleSelectPrompt}
          loading={loading}
          error={error}
          emptyMessage={getEmptyMessage()}
        />
      )}

      {/* Prompt Form Modal */}
      <Modal
        isOpen={showPromptForm}
        onClose={() => {
          setShowPromptForm(false);
          setEditingPrompt(null);
        }}
        title={editingPrompt ? 'Edit Prompt' : 'Create New Prompt'}
      >
        <PromptForm
          promptId={editingPrompt?.id}
          onSuccess={handlePromptSuccess}
          onCancel={() => {
            setShowPromptForm(false);
            setEditingPrompt(null);
          }}
        />
      </Modal>

      {/* Collection Form Modal */}
      <Modal
        isOpen={showCollectionForm}
        onClose={() => setShowCollectionForm(false)}
        title="Create New Collection"
      >
        <CollectionForm
          onSuccess={handleCollectionSuccess}
          onCancel={() => setShowCollectionForm(false)}
        />
      </Modal>
    </Layout>
  );
}

export default App;
