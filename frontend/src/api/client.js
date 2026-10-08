/**
 * Base API client with fetch wrapper and error handling
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Fetch wrapper with consistent error handling
 * 
 * @param {string} endpoint - API endpoint (without base URL)
 * @param {object} options - Fetch options
 * @returns {Promise<any>} - Response data
 * @throws {ApiError} - On HTTP errors or network failures
 */
export async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    // Handle 204 No Content (e.g., DELETE responses)
    if (response.status === 204) {
      return null;
    }

    // Parse JSON response
    const data = await response.json().catch(() => ({}));

    // Handle HTTP errors
    if (!response.ok) {
      const message = data.detail || `HTTP ${response.status} error`;
      throw new ApiError(message, response.status, data);
    }

    return data;
  } catch (error) {
    // Network errors or ApiError
    if (error instanceof ApiError) {
      throw error;
    }
    
    // Network failure
    throw new ApiError(
      'Network error. Check your connection.',
      0,
      null
    );
  }
}

export default apiRequest;
