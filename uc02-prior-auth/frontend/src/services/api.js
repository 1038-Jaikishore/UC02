const BASE_URL = 'http://localhost:8000';

/**
 * Handle fetch response wrapper
 */
async function handleResponse(response) {
  if (!response.ok) {
    let errorMessage = `HTTP error! Status: ${response.status}`;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        } else if (Array.isArray(errorData.detail)) {
          // Format Pydantic validation errors nicely
          errorMessage = errorData.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
        }
      }
    } catch (e) {
      // JSON parsing failed, stick with status message
    }
    throw new Error(errorMessage);
  }
  return response.json();
}

/**
 * Fetch all prior authorizations
 */
export async function fetchAuthorizations() {
  const response = await fetch(`${BASE_URL}/api/authorizations`);
  return handleResponse(response);
}

/**
 * Fetch a single authorization by ID
 */
export async function fetchAuthorization(id) {
  const response = await fetch(`${BASE_URL}/api/authorizations/${id}`);
  return handleResponse(response);
}

/**
 * Create a new authorization request
 */
export async function createAuthorization(payload) {
  const response = await fetch(`${BASE_URL}/api/authorizations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  return handleResponse(response);
}

/**
 * Update the status of an authorization request (human-in-the-loop audit)
 */
export async function updateAuthorizationStatus(id, status) {
  const response = await fetch(`${BASE_URL}/api/authorizations/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });
  return handleResponse(response);
}

/**
 * Simple connection/health check endpoint
 */
export async function checkHealth() {
  const response = await fetch(`${BASE_URL}/health`);
  return handleResponse(response);
}
