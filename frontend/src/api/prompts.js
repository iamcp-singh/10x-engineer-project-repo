/**
 * API functions for prompt CRUD operations
 */

import apiRequest from './client';

/**
 * Get all prompts with optional filters
 * 
 * @param {object} params - Query parameters
 * @param {string} params.search - Search query
 * @param {string} params.collection_id - Filter by collection
 * @returns {Promise<object>} - {prompts: [], total: number}
 */
export async function getPrompts({ search, collection_id } = {}) {
  const params = new URLSearchParams();
  
  if (search) {
    params.append('search', search);
  }
  if (collection_id) {
    params.append('collection_id', collection_id);
  }
  
  const queryString = params.toString();
  const endpoint = queryString ? `/prompts?${queryString}` : '/prompts';
  
  return apiRequest(endpoint);
}

/**
 * Get a single prompt by ID
 * 
 * @param {string} id - Prompt ID
 * @returns {Promise<object>} - Prompt object
 */
export async function getPrompt(id) {
  return apiRequest(`/prompts/${id}`);
}

/**
 * Create a new prompt
 * 
 * @param {object} data - Prompt data
 * @param {string} data.title - Prompt title (required)
 * @param {string} data.content - Prompt content (required)
 * @param {string} data.description - Prompt description (optional)
 * @param {string} data.collection_id - Collection ID (optional)
 * @param {string[]} data.tags - Tags (optional)
 * @returns {Promise<object>} - Created prompt
 */
export async function createPrompt(data) {
  return apiRequest('/prompts', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Update an existing prompt (full update)
 * 
 * @param {string} id - Prompt ID
 * @param {object} data - Full prompt data
 * @returns {Promise<object>} - Updated prompt
 */
export async function updatePrompt(id, data) {
  return apiRequest(`/prompts/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Partially update a prompt
 * 
 * @param {string} id - Prompt ID
 * @param {object} data - Partial prompt data
 * @returns {Promise<object>} - Updated prompt
 */
export async function patchPrompt(id, data) {
  return apiRequest(`/prompts/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

/**
 * Delete a prompt
 * 
 * @param {string} id - Prompt ID
 * @returns {Promise<null>}
 */
export async function deletePrompt(id) {
  return apiRequest(`/prompts/${id}`, {
    method: 'DELETE',
  });
}
