/**
 * API functions for collection operations
 */

import apiRequest from './client';

/**
 * Get all collections
 * 
 * @returns {Promise<object>} - {collections: [], total: number}
 */
export async function getCollections() {
  return apiRequest('/collections');
}

/**
 * Get a single collection by ID
 * 
 * @param {string} id - Collection ID
 * @returns {Promise<object>} - Collection object
 */
export async function getCollection(id) {
  return apiRequest(`/collections/${id}`);
}

/**
 * Create a new collection
 * 
 * @param {object} data - Collection data
 * @param {string} data.name - Collection name (required)
 * @param {string} data.description - Collection description (optional)
 * @returns {Promise<object>} - Created collection
 */
export async function createCollection(data) {
  return apiRequest('/collections', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Delete a collection
 * 
 * @param {string} id - Collection ID
 * @returns {Promise<null>}
 */
export async function deleteCollection(id) {
  return apiRequest(`/collections/${id}`, {
    method: 'DELETE',
  });
}
